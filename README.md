# Materials Project XRD Export

## Overview
This project downloads a crystal structure from the Materials Project API and calculates its simulated X-ray diffraction (XRD) pattern with `pymatgen`.

The script standardizes the structure to a conventional cell, calculates the XRD pattern, and exports the result as a CSV file that can be opened in Origin, Excel, or other analysis software.

## Current Configuration
The main settings are defined near the top of `Material_project.py`:

```python
RADIATION_SOURCE = "CuKa"
MATERIAL_IDS = ["mp-2723"]
```

- `MATERIAL_IDS` controls which Materials Project structures are downloaded. Add more IDs to export multiple XRD patterns in one run.
- `RADIATION_SOURCE` controls the X-ray source used by `XRDCalculator`.
- For `"CuKa"`, `pymatgen` resolves the wavelength internally as `1.54184` angstrom.
- A custom numeric wavelength can also be passed to `XRDCalculator` if needed.

## Features
- Retrieves a crystal structure from Materials Project by material ID.
- Converts the structure to the conventional standard cell for consistent Miller index labels.
- Calculates a simulated XRD pattern using `pymatgen.analysis.diffraction.xrd.XRDCalculator`.
- Uses `pattern.d_hkls` from `XRDCalculator` for d-spacing values.
- Exports material ID, formula, radiation source, wavelength, 2theta, intensity, d-spacing, and HKL labels to CSV.
- Names the output CSV using both the chemical formula and Materials Project ID.
- Prints the same XRD peak information to the console after saving each CSV file.

## Project Structure
```text
Random_things/
|-- Material_project.py
|-- README.md
|-- environment.yml
`-- data/
    `-- download/
```

## Environment Setup
Create the conda environment from `environment.yml`:

```powershell
conda env create -f environment.yml
```

Activate the environment:

```powershell
conda activate random_things
```

If the environment already exists, update it with:

```powershell
conda env update -n random_things --file environment.yml --prune
```

## Usage
Run the script from the project root:

```powershell
python Material_project.py
```

Or run it without activating the environment:

```powershell
conda run -n random_things python Material_project.py
```

On Windows, if `conda run` reports a temporary-file access conflict, activate the environment first and then run `python Material_project.py`.

To export a different material, edit `MATERIAL_IDS` in `Material_project.py`:

```python
MATERIAL_IDS = ["mp-101"]
```

To export multiple materials in one run:

```python
MATERIAL_IDS = ["mp-2723", "mp-101"]
```

## Output
For the current configuration:

```python
MATERIAL_IDS = ["mp-2723"]
RADIATION_SOURCE = "CuKa"
```

the output file is:

```text
data/download/IrO2_xrd_pattern_mp-2723.csv
```

The CSV columns are:

- `material_id`: Materials Project ID, such as `mp-2723`
- `formula`: reduced chemical formula, such as `IrO2`
- `radiation_source`: X-ray source passed to `XRDCalculator`
- `wavelength_angstrom`: wavelength resolved by `XRDCalculator`
- `two_theta`: simulated 2theta diffraction angle in degrees
- `intensity`: relative peak intensity
- `d_spacing_angstrom`: interplanar spacing for the HKL peak
- `hkls`: Miller indices assigned to the peak

Example:

```text
material_id,formula,radiation_source,wavelength_angstrom,two_theta,intensity,d_spacing_angstrom,hkls
mp-2723,IrO2,CuKa,1.54184,28.00816418028475,100.0,3.1857379888508084,"(1, 1, 0)"
```

The script also prints the same peak information in the terminal:

```text
Material ID: mp-2723
Formula: IrO2
Radiation source: CuKa
Wavelength (angstrom): 1.54184
XRD pattern saved to: data/download/IrO2_xrd_pattern_mp-2723.csv

   two_theta     intensity     d_spacing  hkls
----------------------------------------------------------
   28.008164    100.000000      3.185738  (1, 1, 0)
```

## Notes
- A valid Materials Project API key is required.
- The API key is currently provided directly in `Material_project.py`.
- Output files are written to `data/download/`.
- `data/` is ignored by Git, so generated CSV files are not committed by default.
