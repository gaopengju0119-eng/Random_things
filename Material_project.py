### Material_project_download_XRD

import csv
import os

from mp_api.client import MPRester
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


# Radiation source configuration.
# Use a pymatgen-supported source name, such as "CuKa", or a numeric
# wavelength in angstroms for a custom source.
RADIATION_SOURCE = "CuKa"
MATERIAL_ID = "mp-2723"

# Create output directory if it doesn't exist
output_dir = r"C:\Download\Pycharm code\Random_things\data\download"
os.makedirs(output_dir, exist_ok=True)


with MPRester(api_key="VhG42T1WDDotMqdqcbId4MJGJVblvtgP") as mpr:
    # first retrieve the relevant structure
    structure = mpr.get_structure_by_material_id(MATERIAL_ID)
formula = structure.composition.reduced_formula

# important to use the conventional structure to ensure
# that peaks are labeled with the conventional Miller indices
sga = SpacegroupAnalyzer(structure)
conventional_structure = sga.get_conventional_standard_structure()

# this example shows how to obtain an XRD diffraction pattern
# these patterns are calculated on-the-fly from the structure
calculator = XRDCalculator(wavelength=RADIATION_SOURCE)
pattern = calculator.get_pattern(conventional_structure)
wavelength_angstrom = calculator.wavelength

# Save XRD pattern data as CSV for easy import into Origin
pattern_file = os.path.join(output_dir, f"{formula}_xrd_pattern_{MATERIAL_ID}.csv")
with open(pattern_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "material_id",
            "formula",
            "radiation_source",
            "wavelength_angstrom",
            "two_theta",
            "intensity",
            "d_spacing_angstrom",
            "hkls",
        ]
    )
    for two_theta, intensity, d_spacing, hkls in zip(
        pattern.x, pattern.y, pattern.d_hkls, pattern.hkls
    ):
        hkl_labels = "; ".join(str(item["hkl"]) for item in hkls)
        writer.writerow(
            [
                MATERIAL_ID,
                formula,
                RADIATION_SOURCE,
                wavelength_angstrom,
                two_theta,
                intensity,
                d_spacing,
                hkl_labels,
            ]
        )

print(f"XRD pattern saved to: {pattern_file}")
