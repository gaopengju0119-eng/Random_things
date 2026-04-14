# Material Project - XRD Download and Analysis

## Overview
This project downloads crystal structure data from the Materials Project API and calculates X-ray diffraction (XRD) patterns using PyMatGen.

## Features
- **Materials Project Integration**: Retrieves crystal structures by material ID using the Materials Project REST API
- **Structure Standardization**: Converts structures to conventional standard form to ensure proper Miller indices labeling
- **XRD Calculation**: Calculates X-ray diffraction patterns using CuKα radiation
- **CSV Export**: Saves XRD pattern data (2θ angles, intensity, Miller indices) for import into Origin or other analysis software

## Project Structure
```
Random_things/
├── Material_project.py      # Main script for XRD analysis
├── README.md               # This file
├── environment.yml         # Conda environment specification
└── data/
    └── download/          # Output directory for XRD patterns
```

## Dependencies
- **python**: 3.13.13
- **mp-api**: Materials Project API client
- **pymatgen**: Python Materials Genomics - for crystal structure analysis and XRD calculations

## Usage
1. Ensure conda environment is set up with dependencies
2. Run the script: `python Material_project.py`
3. Output XRD pattern CSV file will be saved to `data/download/`

## Output
The script generates a CSV file with columns:
- `two_theta`: 2θ diffraction angle (degrees)
- `intensity`: Relative intensity
- `hkls`: Miller indices for the diffraction peak

## Notes
- Requires a valid Materials Project API key
- Currently configured for material ID: mp-2723 (Example structure)
- Uses conventional structure representation for accurate peak indexing
