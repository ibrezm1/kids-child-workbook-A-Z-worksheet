# Child Worksheet Generator

This project generates PDF worksheets for children to practice writing letters and numbers. It creates tracing exercises using specific educational fonts.

## Features

- Generates a PDF workbook (`alphabet_workbook.pdf`)
- Includes pages for:
  - Uppercase Letters (A-Z)
  - Numbers (0-9)
- Uses dotted fonts for tracing practice
- 3-line writing guidelines with dashed middle line

## Prerequisites

- Python 3.x
- `reportlab` library
- Required Fonts (placed in the project directory):
  - `KGPrimaryDots.ttf` (for tracing)
  - `Andika-Regular.ttf` (for solid headers)

## Font Licenses

- **Andika**: Licensed under the [SIL Open Font License (OFL)](https://scripts.sil.org/OFL). You are free to use, modify, and redistribute it.
- **KG Primary Dots**: Free for **personal use only**. If you plan to sell these worksheets or use them commercially, you must purchase a license from [Kimberly Geswein Fonts](http://kimberlygeswein.com).

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install reportlab
   ```
   *Note: If you are using the `.venv`, ensure you activate it before installing.*

## Usage

Run the script to generate the workbook:

```bash
python generate_worksheet.py
```

The output file `alphabet_workbook.pdf` will be created in the same directory.
