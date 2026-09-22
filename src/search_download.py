"""Search and download NASA HLS (Harmonized Landsat Sentinel-2) granules for the AOI.

HLS provides 30 m surface reflectance from both Landsat 8/9 and Sentinel-2,
composited to a common grid — higher revisit frequency than Landsat alone,
which matters here since we need one clear (low-cloud) scene shortly before
and shortly after Helene (landfall 2024-09-27).

Requires a free NASA Earthdata Login: https://urs.earthdata.nasa.gov/
On first run, earthaccess.login() will prompt for credentials and cache them
in ~/.netrc.
"""
import argparse
from pathlib import Path

import earthaccess
import geopandas as gpd


def load_aoi_bbox(geojson_path: str) -> tuple[float, float, float, float]:
    gdf = gpd.read_file(geojson_path)
    return tuple(gdf.total_bounds)  # (minx, miny, maxx, maxy)


def search_hls_granules(
    aoi_geojson_path: str,
    date_start: str,
    date_end: str,
    short_name: str = "HLSL30",
    cloud_cover_max: int = 20,
):
    """short_name: 'HLSL30' (Landsat-derived) or 'HLSS30' (Sentinel-2-derived)."""
    bbox = load_aoi_bbox(aoi_geojson_path)
    results = earthaccess.search_data(
        short_name=short_name,
        bounding_box=bbox,
        temporal=(date_start, date_end),
        cloud_cover=(0, cloud_cover_max),
    )
    return results


def download_granules(results, out_dir: str):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    return earthaccess.download(results, out_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aoi", default="config/aoi_swannanoa.geojson")
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument("--product", default="HLSL30", choices=["HLSL30", "HLSS30"])
    parser.add_argument("--max-cloud", type=int, default=20)
    parser.add_argument("--out", default="data/raw")
    args = parser.parse_args()

    earthaccess.login()  # prompts once, then reuses cached ~/.netrc credentials
    granules = search_hls_granules(args.aoi, args.start, args.end, args.product, args.max_cloud)
    print(f"Found {len(granules)} granule(s) for {args.product} between {args.start} and {args.end}")
    for g in granules:
        print(" -", g["meta"]["native-id"])

    if granules:
        download_granules(granules, args.out)
