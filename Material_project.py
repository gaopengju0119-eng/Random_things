### Material_project_download_XRD

import csv
import os
import re

from mp_api.client import MPRester
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


# Change this list to export XRD patterns for other Materials Project entries.
# Example: MATERIAL_IDS = ["mp-2723", "mp-101"]
MATERIAL_IDS = ["mp-2723"]

# Use a pymatgen-supported source name, such as "CuKa", or a numeric
# wavelength in angstroms for a custom source.
RADIATION_SOURCE = "CuKa"

API_KEY = "VhG42T1WDDotMqdqcbId4MJGJVblvtgP"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data", "download")

CSV_COLUMNS = [
    "material_id",
    "formula",
    "radiation_source",
    "wavelength_angstrom",
    "two_theta",
    "intensity",
    "d_spacing_angstrom",
    "hkls",
]


def safe_filename(value):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def get_conventional_structure(structure):
    # Conventional cells give more consistent Miller index labels.
    analyzer = SpacegroupAnalyzer(structure)
    return analyzer.get_conventional_standard_structure()


def get_xrd_rows(material_id, structure, radiation_source):
    formula = structure.composition.reduced_formula
    conventional_structure = get_conventional_structure(structure)

    calculator = XRDCalculator(wavelength=radiation_source)
    pattern = calculator.get_pattern(conventional_structure)
    wavelength_angstrom = calculator.wavelength

    rows = []
    for two_theta, intensity, d_spacing, hkls in zip(
        pattern.x, pattern.y, pattern.d_hkls, pattern.hkls
    ):
        hkl_labels = "; ".join(str(item["hkl"]) for item in hkls)
        rows.append(
            {
                "material_id": material_id,
                "formula": formula,
                "radiation_source": radiation_source,
                "wavelength_angstrom": wavelength_angstrom,
                "two_theta": two_theta,
                "intensity": intensity,
                "d_spacing_angstrom": d_spacing,
                "hkls": hkl_labels,
            }
        )
    return formula, rows


def save_xrd_csv(output_dir, material_id, formula, rows):
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{safe_filename(formula)}_xrd_pattern_{safe_filename(material_id)}.csv"
    pattern_file = os.path.join(output_dir, filename)

    with open(pattern_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    return pattern_file


def print_xrd_rows(material_id, formula, rows, pattern_file):
    print()
    print(f"Material ID: {material_id}")
    print(f"Formula: {formula}")
    print(f"Radiation source: {rows[0]['radiation_source']}")
    print(f"Wavelength (angstrom): {rows[0]['wavelength_angstrom']}")
    print(f"XRD pattern saved to: {pattern_file}")
    print()
    print(
        f"{'two_theta':>12}  {'intensity':>12}  "
        f"{'d_spacing':>12}  {'hkls'}"
    )
    print("-" * 58)

    for row in rows:
        print(
            f"{row['two_theta']:12.6f}  "
            f"{row['intensity']:12.6f}  "
            f"{row['d_spacing_angstrom']:12.6f}  "
            f"{row['hkls']}"
        )


def main():
    with MPRester(api_key=API_KEY) as mpr:
        for material_id in MATERIAL_IDS:
            structure = mpr.get_structure_by_material_id(material_id)
            formula, rows = get_xrd_rows(material_id, structure, RADIATION_SOURCE)
            pattern_file = save_xrd_csv(OUTPUT_DIR, material_id, formula, rows)
            print_xrd_rows(material_id, formula, rows, pattern_file)


if __name__ == "__main__":
    main()
