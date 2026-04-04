# This contains the files for a simple exercise on Custom Land Cover in Trends.Earth

# Exercise: Custom Land Cover Analysis with Trends.Earth
### YINCHUAN GLC_FSC30 (https://doi.org/10.5194/essd-13-2753-2021) Aerospace Institute CCAS → UNCCD 7 Classes

This repository contains all materials to replicate a custom land cover 
degradation analysis using [Trends.Earth](https://trends.earth) (QGIS plugin), 
based on the GLC_FSC30 Land Cover dataset, sset for Yinchuan and reclassified to the 7 UNCCD classes. It follows the same workflow 
as the [Conservation International MapBiomas tutorial](https://www.youtube.com/watch?v=3uiGdP1qrK8), 
adapted for the Mongolia national classification.

## Contents

| File | Description |
|------|-------------|
| `data/Mongolia_LC_2001_original.tif` | Original LC raster, year 2001 |
| `data/Mongolia_LC_2015_original.tif` | Original LC raster, year 2015 |
| `data/Mongolia_LC_2020_original.tif` | Original LC raster, year 2020 |
| `data/Mongolia_AOI_geometry.geojson` | Area of interest |
| `trendsearth/Mongolia_LC_legend.json` | Custom legend — load in Trends.Earth Settings |
| `trendsearth/Mongolia_LC_nesting.json` | Nesting definition — maps Mongolia classes to UNCCD 7 |
| `trendsearth/lc_degradation_stats.py` | QGIS Python script to compute statistics |
| `qgis/Mongolia_LC_original.qml` | QGIS style file for the original LC legend |
| `gee/mongolia_lc_export_original.js` | Google Earth Engine export script |
| `tables/mongolia_reclass.xlsx` | Reclassification table original → UNCCD 7 classes |

## Data Sources

- **Mongolia National Land Cover**: dowbloaded from [Apacheta](http://www.apacheta.org) — 
licensed under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
- **Trends.Earth**: Conservation International, Lund University, NASA
- **UNCCD 7-class framework**: UNCCD Good Practice Guidance

## Workflow

1. Set the AOI using `Mongolia_AOI_geometry.geojson` under Trends.Eart setting /Area from file
2. Load the two rasters (CTRL-SHIFT R) in QGIS and apply the `.qml` style
3. Go to **Trends.Earth/Datasets  → Import datasets ** Import custom land cover dataset (tif) - set year (2000) and resolution (250m) 
4. Choose a land cover aggregation method - ready Load definition from file: reclass_sset_mongolia.json
5. Repeat the same for 2015 land cover and 2020 land cover 
6. Go to Algorithms - Land cover change  - Execute locally -  set initial (2000) and target (2015) files just created - name the execution
7. Repeat the same for LC 2015 to 2020 (reporting period)
8. Try changing the transition matrix  - no default interpretation - a modified transition matrix is added as an example (transtiion_sset_mongolia.json)
9. Go to Algorthms - Land Cover Change - Execute locally - com[pute land cover change and degradation for the baseline (2000-2015) and for the reporting period (2015-2020)
10. ActivateLand Compute statistics algorithm (local execution) using `lc_degradation_stats.py` in the QGIS Python Console

## Download all files
<CODE> Download zip files
