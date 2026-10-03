# Vegetation Change (NDVI) Along the Swannanoa River Valley: Hurricane Helene (2024)

A geospatial analysis of NDVI-based vegetation change in the Swannanoa River
valley (Black Mountain → Asheville, NC) using NASA satellite imagery.

**Phase 1 (complete)** compares conditions shortly before and after Hurricane
Helene (landfall 2024-09-27) to identify areas of substantial negative
vegetation change. **Phase 2 (planned)** extends the analysis through
2025–2026 to examine vegetation recovery across the same corridor.

## Why this project

Hurricane Helene is personal to me. I was living in the Asheville area when
the storm hit Western North Carolina, and when I was able to, I drove through
the surrounding areas. I saw roads and restaurants broken into pieces. Since
then the roads have been fixed, but the restaurants have been left abandoned,
waiting for new owners to buy and rebuild them. Recovery didn't look the same
everywhere.

That made me want to see what the landscape itself looked like from above.
Two years later, rather than only reading about the rebuilding, I wanted to
use the skills I've been developing to study a small part of it myself. This
is my first hands-on remote-sensing project: it measures how vegetation along
the Swannanoa River Valley changed in the weeks right after the storm.
Phase 2 extends it to tracking recovery over time.

I came into this with a CS degree, a Biology minor, and some GIS training
(ESRI/ArcGIS) from coursework and botanical fieldwork — but no prior
hands-on experience with satellite or Earth observation data. I built this
project to close that gap ahead of applying to NASA's EarthRISE Developers
Academy: to prove to myself, not just claim on an application, that I can
take a real disaster event, pull the actual NASA imagery, and turn it into
a defensible, quantified result end to end.

## Background

Helene's remnants dropped record rainfall on the Southern Appalachians in
late September 2024, causing catastrophic flooding and debris flows along
the Swannanoa and French Broad Rivers. Buncombe County, NC — including
Black Mountain, Swannanoa, and Biltmore Village in Asheville — saw some of
the most severe damage to riparian forest and urban tree canopy in the
region.

This project measures vegetation change using the Normalized
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
- **Pre-event:** 2024-08-30 (HLS.L30.T17SLV, 17% cloud cover — the clearest
  Landsat pass available between May and landfall; every scene in the two
  weeks directly before Helene was 58%+ cloudy)
- **Post-event:** 2024-10-09 (HLS.L30.T17SLV, 0% cloud cover, 12 days after
  landfall)
- **Bands used:** Red and Near-Infrared (NDVI), plus the Fmask quality band
  for cloud/cloud-shadow/snow masking.

Both scenes are HLSL30 (Landsat 9) on the same MGRS tile, chosen
deliberately to avoid cross-sensor NDVI differences between Landsat and
Sentinel-2.

Raw and processed imagery are not committed to this repo (see
`.gitignore`) — they're large and fully reproducible via
[`src/search_download.py`](src/search_download.py).

## Method

1. **Search & download** matching HLS granules for the AOI and date
   windows (`src/search_download.py`).
2. **Compute NDVI** = (NIR − Red) / (NIR + Red) for each date, masking out
   cloud/shadow/snow pixels using the Fmask QA band (`src/ndvi.py`).
3. **Difference** the two NDVI rasters (post − pre); negative values
   indicate lower NDVI (possible vegetation loss, stress, or seasonal
   change).
4. **Quantify and visualize**: side-by-side NDVI maps, a diverging
   difference map, and a histogram of the change distribution with a
   ΔNDVI threshold (`src/plotting.py`).

Full walkthrough in
[`notebooks/01_ndvi_before_after.ipynb`](notebooks/01_ndvi_before_after.ipynb).

## Results — Phase 1: Immediate Change

| | Pre-Helene (2024-08-30) | Post-Helene (2024-10-09) |
|---|---|---|
| Mean NDVI (AOI, unmasked pixels) | 0.81 | 0.74 |

**11.5%** of valid pixels across the AOI show ΔNDVI < -0.15, the threshold used
here for "substantial negative vegetation change." Valid means unmasked in
both scenes.

![Pre/post NDVI and difference map](outputs/figures/ndvi_before_after_diff.png)

The difference map (right panel) shows a clear, continuous band of
negative NDVI change tracing the Swannanoa River channel itself — consistent
with flood scouring and debris flows along the waterway — plus more
diffuse, scattered negative change across the surrounding hillsides, possibly
from wind damage. These interpretations are visual and not validated (see
limitations below).

![NDVI change histogram](outputs/figures/ndvi_change_histogram.png)

## Limitations (Phase 1)

This is a two-scene snapshot, not a time series, and it's honest to be
upfront about what that does and doesn't support:

- **Single before/after pair.** A cloud-free Landsat pass wasn't available
  in the two weeks immediately before landfall (every scene was 58%+
  cloudy), so the pre-event baseline is from Aug 30 — about four weeks
  before Helene. Normal late-summer phenology could account for part of the
  observed NDVI drop, not just storm damage; this analysis can't say how much.
- **No ground truth.** The change threshold (ΔNDVI < -0.15) is a reasonable
  convention, not validated against field survey or high-resolution
  post-storm aerial imagery of this specific corridor.
- **Wind vs. flood damage aren't separated.** The river-channel band of
  negative change and the diffuse hillside change are visually
  distinguishable but not quantified as separate categories.
- **Scene means aren't computed over identical pixels.** Each mean NDVI
  value (0.81 and 0.74) is averaged over that scene's own unmasked pixels,
  and the Aug 30 scene is 17% cloudy, so more of it is masked. The 11.5%
  figure uses only pixels unmasked in both scenes and is the more reliable
  comparison.

## Phase 2 — Two Years of Recovery (planned)

Phase 1 stands as a complete before/after comparison. Phase 2 extends the
project from immediate impact to recovery over the two years since landfall.
It has not been started; the planned analysis is:

1. Build seasonal or monthly HLS composites spanning 2024–2026.
2. Replace the single Aug 30 baseline with a multi-observation pre-Helene
   baseline, to separate the storm signal from normal seasonal variation.
3. Measure NDVI trajectories in the areas with the largest initial negative
   change.
4. Compare recovery along the river corridor with surrounding areas.
5. Overlay independent hazard data (USGS/NOAA flood extent, NC landslide
   inventory) to separate flood-driven change from wind-driven change.
6. Validate a subset of the corridor against higher-resolution imagery
   (e.g., NAIP or commercial post-storm aerials).
7. Identify areas where NDVI has returned toward its pre-storm range and
   areas where negative differences persist.

The goal is not to label an area "recovered" based on NDVI alone, but to
investigate how remotely sensed vegetation conditions have changed over the
two years following Helene.

## Setup

Requires a free [NASA Earthdata Login](https://urs.earthdata.nasa.gov/)
account.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# First run prompts for Earthdata credentials and caches them in ~/.netrc
python src/search_download.py --start 2024-08-29 --end 2024-08-31 --max-cloud 20
python src/search_download.py --start 2024-10-08 --end 2024-10-10 --max-cloud 20

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

## License

MIT
