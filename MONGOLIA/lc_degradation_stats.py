"""
Land Cover Degradation Statistics
----------------------------------
Run this script in QGIS Python Console:
  Plugins > Python Console > paste and run

It reads the active raster layer (your LC degradation output),
counts pixels per class, computes areas in km2, and prints a
summary table. Optionally saves results to a CSV file.

LC Degradation class codes (Trends.Earth standard):
  -1 = Degraded
   0 = Stable
   1 = Improved
  -32768 = No Data
"""

from qgis.core import QgsProject, QgsRasterLayer
import numpy as np
import os

# ── CONFIG ──────────────────────────────────────────────────────────
# Set to None to use the currently active layer,
# or set a layer name string e.g. "LC_degradation_2001_2015"
LAYER_NAME = None

# Output CSV path — set to None to skip saving
OUTPUT_CSV = r"C:/Users/Conchedda/OneDrive - Food and Agriculture Organization/NSL/PRAIS_tools/CHN/EXERCISE_LC/MONGOLIA/lc_degradation_stats.csv"
# ────────────────────────────────────────────────────────────────────

CLASS_LABELS = {
    -1:     "Degraded",
    0:      "Stable",
    1:      "Improved",
    -32768: "No Data"
}

def get_layer(name):
    if name:
        layers = QgsProject.instance().mapLayersByName(name)
        if not layers:
            raise ValueError(f"Layer '{name}' not found in project.")
        return layers[0]
    layer = iface.activeLayer()
    if not layer or not isinstance(layer, QgsRasterLayer):
        raise ValueError("No raster layer is currently active. Select your LC degradation layer first.")
    return layer

def read_raster_as_array(layer):
    provider = layer.dataProvider()
    block = provider.block(1, layer.extent(), layer.width(), layer.height())
    data = np.array([block.value(row, col)
                     for row in range(layer.height())
                     for col in range(layer.width())], dtype=np.float64)
    return data.reshape(layer.height(), layer.width())

def compute_pixel_area_km2(layer):
    """Compute area of one pixel in km2, handling geographic and projected CRS."""
    crs = layer.crs()
    x_res = layer.rasterUnitsPerPixelX()
    y_res = layer.rasterUnitsPerPixelY()
    if crs.isGeographic():
        # degrees — approximate conversion at centre latitude
        extent = layer.extent()
        centre_lat = (extent.yMinimum() + extent.yMaximum()) / 2.0
        lat_rad = np.radians(centre_lat)
        x_km = x_res * 111.32 * np.cos(lat_rad)
        y_km = y_res * 110.574
        return abs(x_km * y_km)
    else:
        # projected — units are metres
        return abs((x_res / 1000.0) * (y_res / 1000.0))

def run():
    layer = get_layer(LAYER_NAME)
    print(f"\n{'='*55}")
    print(f"  Layer : {layer.name()}")
    print(f"  CRS   : {layer.crs().authid()}")
    print(f"  Size  : {layer.width()} x {layer.height()} pixels")

    print("  Reading raster data...")
    arr = read_raster_as_array(layer)
    pixel_km2 = compute_pixel_area_km2(layer)
    print(f"  Pixel area: {pixel_km2:.6f} km²")

    # ── Count pixels per class ───────────────────────────────────────
    unique, counts = np.unique(arr, return_counts=True)
    value_counts = dict(zip(unique.astype(int), counts))

    # ── Build results ────────────────────────────────────────────────
    results = []
    total_valid = 0
    for code, label in CLASS_LABELS.items():
        count = value_counts.get(code, 0)
        area  = count * pixel_km2
        results.append((code, label, count, area))
        if code != -32768:
            total_valid += area

    # ── Print summary ────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print(f"  {'Code':>7}  {'Class':<12}  {'Pixels':>10}  {'Area (km²)':>12}  {'%':>6}")
    print(f"  {'-'*7}  {'-'*12}  {'-'*10}  {'-'*12}  {'-'*6}")
    for code, label, count, area in results:
        pct = (area / total_valid * 100) if total_valid > 0 and code != -32768 else 0
        pct_str = f"{pct:.1f}%" if code != -32768 else "  —"
        print(f"  {code:>7}  {label:<12}  {count:>10,}  {area:>12.2f}  {pct_str:>6}")
    print(f"  {'':>7}  {'TOTAL (valid)':<12}  {'':>10}  {total_valid:>12.2f}  {'100.0%':>6}")
    print(f"{'='*55}\n")

    # ── Save CSV ─────────────────────────────────────────────────────
    if OUTPUT_CSV:
        import csv
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        with open(OUTPUT_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Code', 'Class', 'Pixel Count', 'Area_km2', 'Percent'])
            for code, label, count, area in results:
                pct = (area / total_valid * 100) if total_valid > 0 and code != -32768 else ''
                writer.writerow([code, label, count, round(area, 4), round(pct, 2) if pct != '' else ''])
        print(f"  Results saved to:\n  {OUTPUT_CSV}\n")

run()
