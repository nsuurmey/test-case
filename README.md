# Matlab to Python Converter

This is a simple script to convert basic Matlab code to Python.

## Features

- Converts `%` comments to `#`
- Removes trailing semicolons
- Converts `if/elseif/else` statements
- Converts basic `for` loops
- Converts matrices to `numpy` arrays
- Handles indentation for blocks

## Usage

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the converter:**

   ```bash
   python converter.py <input_matlab_file.m> <output_python_file.py>
   ```

   For example:

   ```bash
   python converter.py sample.m sample_converted.py
   ```
