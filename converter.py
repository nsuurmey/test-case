import re
import sys

def convert_matlab_to_python(matlab_code):
    python_code = []
    lines = matlab_code.splitlines()
    indent_level = 0
    numpy_imported = False

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            python_code.append("")
            continue

        # Handle block endings first
        if re.match(r'^\s*end\s*$', stripped_line):
            indent_level = max(0, indent_level - 1)
            continue

        # Handle else/elseif, which dedent before the line
        if re.match(r'^\s*elseif.*', stripped_line) or re.match(r'^\s*else\s*$', stripped_line):
            indent_level = max(0, indent_level - 1)

        # Apply indentation
        output_line = '    ' * indent_level + stripped_line

        # Convert comments
        output_line = output_line.replace('%', '#', 1)

        # Remove trailing semicolons
        if output_line.endswith(';'):
            output_line = output_line[:-1]

        # If statements
        if_match = re.match(r'^\s*if\s+(.*)', stripped_line)
        if if_match:
            condition = if_match.group(1)
            output_line = '    ' * indent_level + f'if {condition}:'
            indent_level += 1

        # Elseif statements
        elseif_match = re.match(r'^\s*elseif\s+(.*)', stripped_line)
        if elseif_match:
            condition = elseif_match.group(1)
            output_line = '    ' * indent_level + f'elif {condition}:'
            indent_level += 1

        # Else statements
        if re.match(r'^\s*else\s*$', stripped_line):
            output_line = '    ' * indent_level + 'else:'
            indent_level += 1

        # For loops (basic form: for i = 1:10)
        for_match = re.match(r'^\s*for\s+(\w+)\s*=\s*(\d+):(\d+)', stripped_line)
        if for_match:
            var, start, end = for_match.groups()
            output_line = '    ' * indent_level + f'for {var} in range({start}, {int(end) + 1}):'
            indent_level += 1

        # Matrix definition
        matrix_match = re.match(r'(\w+\s*=\s*)\[(.*)\]', stripped_line)
        if matrix_match:
            if not numpy_imported:
                python_code.insert(0, 'import numpy as np')
                numpy_imported = True
            var_assign = matrix_match.group(1)
            content = matrix_match.group(2)
            # Convert Matlab matrix content to Python list of lists
            py_content = content.replace(';', '], [')
            output_line = '    ' * indent_level + f'{var_assign}np.array([[{py_content}]])'

        # disp function
        if 'disp(' in output_line:
            output_line = output_line.replace('disp(', 'print(')

        python_code.append(output_line)

    return '\n'.join(python_code)

def main():
    if len(sys.argv) != 3:
        print("Usage: python converter.py <input_matlab_file> <output_python_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        matlab_code = f.read()

    python_code = convert_matlab_to_python(matlab_code)

    with open(output_file, 'w') as f:
        f.write(python_code)

    print(f"Successfully converted {input_file} to {output_file}")

if __name__ == "__main__":
    main()
