"""NDVI computation and cloud/shadow masking for NASA HLS scenes.

Band naming differs between the two HLS products:
  HLSL30 (Landsat-derived):   red = B04, NIR = B05
  HLSS30 (Sentinel-2-derived): red = B04, NIR = B8A
"""
import numpy as np
import rasterio
import rioxarray as rxr
from rasterio.enums import Resampling

# Fmask QA bit flags (HLS v2.0). A pixel is unusable if any of these bits are set.
FMASK_CLOUD_BIT = 1
FMASK_ADJACENT_BIT = 2
FMASK_SHADOW_BIT = 3
FMASK_SNOW_BIT = 4

BAD_PIXEL_MASK = (
    (1 << FMASK_CLOUD_BIT)
    | (1 << FMASK_ADJACENT_BIT)
    | (1 << FMASK_SHADOW_BIT)
    | (1 << FMASK_SNOW_BIT)
)


def read_band(path: str, aoi_bounds=None):
    """Read a single-band HLS GeoTIFF, optionally clipped to (minx, miny, maxx, maxy) in WGS84."""
    da = rxr.open_rasterio(path, masked=True).squeeze()
    if aoi_bounds is not None:
        da = da.rio.clip_box(*aoi_bounds, crs="EPSG:4326")
    return da


def compute_ndvi(red_path: str, nir_path: str, fmask_path: str | None = None, aoi_bounds=None):
    """Return an NDVI DataArray in [-1, 1], with clouded/shadowed pixels set to NaN."""
    red = read_band(red_path, aoi_bounds).astype("float32")
    nir = read_band(nir_path, aoi_bounds).astype("float32")

    ndvi = (nir - red) / (nir + red)
    ndvi = ndvi.where((nir + red) != 0)

    if fmask_path is not None:
        # fillna(255) before casting: NaN (nodata/edge pixels) cast to an int type is
        # undefined and can silently become 0 ("clear"), which would let bad pixels through.
        # 255 has every flag bit set, so those pixels are correctly masked out instead.
        fmask = read_band(fmask_path, aoi_bounds).fillna(255).astype("uint16")
        bad = (fmask.values & BAD_PIXEL_MASK) != 0
        ndvi = ndvi.where(~bad)

    return ndvi.clip(-1, 1)


def align_to(reference, other):
    """Reproject/resample `other` onto `reference`'s grid so pre/post scenes can be subtracted directly."""
    return other.rio.reproject_match(reference, resampling=Resampling.bilinear)


def ndvi_difference(pre_ndvi, post_ndvi):
    """post - pre: negative values indicate a decline in NDVI (possible vegetation loss)."""
    post_aligned = align_to(pre_ndvi, post_ndvi)
    return post_aligned - pre_ndvi
