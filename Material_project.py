### Material_project_download_XRD

import csv
import os

from mp_api.client import MPRester
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


# Create output directory if it doesn't exist
output_dir = r"C:\Download\Pycharm code\Random_things\data\download"
os.makedirs(output_dir, exist_ok=True)

with MPRester(api_key="VhG42T1WDDotMqdqcbId4MJGJVblvtgP") as mpr:
    # first retrieve the relevant structure
    structure = mpr.get_structure_by_material_id("mp-2723")

# important to use the conventional structure to ensure
# that peaks are labeled with the conventional Miller indices
sga = SpacegroupAnalyzer(structure)
conventional_structure = sga.get_conventional_standard_structure()

# this example shows how to obtain an XRD diffraction pattern
# these patterns are calculated on-the-fly from the structure
calculator = XRDCalculator(wavelength="CuKa")
pattern = calculator.get_pattern(conventional_structure)

# Save XRD pattern data as CSV for easy import into Origin
pattern_file = os.path.join(output_dir, "xrd_pattern_mp-2723.csv")
with open(pattern_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["two_theta", "intensity", "hkls"])
    for two_theta, intensity, hkls in zip(pattern.x, pattern.y, pattern.hkls):
        hkl_labels = "; ".join(str(item["hkl"]) for item in hkls)
        writer.writerow([two_theta, intensity, hkl_labels])

print(f"XRD pattern saved to: {pattern_file}")
