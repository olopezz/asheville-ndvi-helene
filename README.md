# Canopy Change Along the Swannanoa River Valley: Hurricane Helene (2024)

A geospatial analysis of vegetation/canopy loss in the Swannanoa River valley
(Black Mountain → Asheville, NC) using NDVI derived from NASA satellite
imagery, comparing conditions shortly before and after Hurricane Helene
(landfall 2024-09-27).

## Background

Helene's remnants dropped record rainfall on the Southern Appalachians in
late September 2024, causing catastrophic flooding and debris flows along
the Swannanoa and French Broad Rivers. Buncombe County, NC — including
Black Mountain, Swannanoa, and Biltmore Village in Asheville — saw some of
the most severe damage to riparian forest and urban tree canopy in the
region.

This project quantifies that vegetation loss using the Normalized
Difference Vegetation Index (NDVI), a standard remote-sensing measure of
plant health and canopy density, computed from satellite surface
reflectance before and after the storm.

## Area of interest

The Swannanoa River corridor, rather than the full county, to keep the
analysis focused on a single watershed with a clear before/after flood
signal. See [`config/aoi_swannanoa.geojson`](config/aoi_swannanoa.geojson).

## Data

- **Source:** [NASA HLS (Harmonized Landsat Sentinel-2)](https://lpdaac.usgs.gov/products/hlsl30v002/),
  v2.0, via NASA's [Earthdata](https://www.earthdata.nasa.gov/) and the
  `earthaccess` Python client. HLS combines Landsat 8/9 and Sentinel-2 into
  a common 30 m grid, giving more frequent clear-sky revisits than Landsat
  alone — important for catching a cloud-free scene in the narrow pre/post
  storm windows.
- **Pre-event:** clearest available scene, mid-Aug – Sept 26, 2024
- **Post-event:** clearest available scene, Sept 28 – late Oct 2024
- **Bands used:** Red and Near-Infrared (NDVI), plus the Fmask quality band
  for cloud/cloud-shadow/snow masking.

Raw and processed imagery are not committed to this repo (see
`.gitignore`) — they're large and fully reproducible via
[`src/search_download.py`](src/search_download.py).

## Method

1. **Search & download** matching HLS granules for the AOI and date
   windows (`src/search_download.py`).
2. **Compute NDVI** = (NIR − Red) / (NIR + Red) for each date, masking out
   cloud/shadow/snow pixels using the Fmask QA band (`src/ndvi.py`).
3. **Difference** the two NDVI rasters (post − pre); negative values
   indicate canopy/vegetation loss.
4. **Quantify and visualize**: side-by-side NDVI maps, a diverging
   difference map, and a histogram of the change distribution with a
   loss-threshold cutoff (`src/plotting.py`).

Full walkthrough in
[`notebooks/01_ndvi_before_after.ipynb`](notebooks/01_ndvi_before_after.ipynb).

### Stretch goal

Overlay USGS/NOAA post-storm flood extent or NC landslide inventory data
on the ΔNDVI raster to separate flood-driven riparian loss from
wind-driven canopy damage upslope.

## Setup

Requires a free [NASA Earthdata Login](https://urs.earthdata.nasa.gov/)
account.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# First run prompts for Earthdata credentials and caches them in ~/.netrc
python src/search_download.py --start 2024-08-15 --end 2024-09-26 --max-cloud 15
python src/search_download.py --start 2024-09-28 --end 2024-10-20 --max-cloud 15

jupyter lab notebooks/01_ndvi_before_after.ipynb
```

## Repository structure

```
config/       AOI definition (GeoJSON)
src/          NDVI computation, HLS search/download, plotting utilities
notebooks/    Main analysis notebook
data/         Downloaded/processed rasters (gitignored)
outputs/      Exported figures
```

## Background & motivation

Built as a portfolio project to demonstrate applied Earth observation
analysis — connecting a CS/Biology background and prior ESRI GIS training
to satellite-based vegetation monitoring.

## License

MIT
