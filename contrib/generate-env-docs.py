#!/usr/bin/env python3
import json
from io import StringIO

JSONMENU_FILENAME = 'docs/environment_variables.json'
OUTPUT_FILENAME = 'docs/environment_variables.rst'
LINE_LENGTH = 75
DESCRIPTION_WRAP_LINES = False


def write_wrapped_lines(description, out):
    remaining = description
    while len(remaining) > 0:
        if len(remaining) > LINE_LENGTH:
            out.write(f'   {remaining[:LINE_LENGTH]}')
            b = remaining[LINE_LENGTH:].split(' ', maxsplit=1)

            if len(b) == 2:
                # More than one line is remaining.  Split the current line
                # at a whitespace
                out.write(b[0])
                out.write('\n')
                remaining = b[1]
            else:
                # Remaining text can't be split, allow line to overflow
                out.write(f'{b[0]}\n')
                break
        else:
            out.write(f'   {remaining}\n')
            break
    remaining = field['description']

    out.write('\n')


if __name__ == '__main__':
    with open(JSONMENU_FILENAME, 'r') as fjson:
        fields = json.load(fjson)

    out = StringIO('')
    out.write('..\n')
    out.write('   This is a generated file; DO NOT EDIT!\n')
    out.write('\n')
    out.write("   Please edit 'config/menu.json' to modify the list of variables and run\n")
    out.write("   './contrib/refresh-docs.sh' to regenerate this file\n")
    out.write('\n')

    out.write('Environment variables\n')
    out.write('^^^^^^^^^^^^^^^^^^^^^\n')
    out.write('\n')

    for variable_index, (variable_name, field) in enumerate(fields.items()):
        if not variable_index == 0:
            # Write delimeter lines
            out.write('\n')
            out.write('\n')

        out.write(f'{variable_name}\n')
        out.write('~' * len(variable_name) + '\n')
        out.write('\n')

        out.write(f":Type: *{field['type']}*\n")

        default = field['default']
        if default in ['None', 'False', 'True', 'Flowgraph-defined']:
            out.write(f':Default: *{default}*\n')
        elif default == '':
            out.write(':Default:\n')
        else:
            out.write(f':Default: ``{default}``\n')

        out.write(f":Required: *{'Yes' if field['required'] else 'No'}*\n")
        out.write(':Description:\n')
        if DESCRIPTION_WRAP_LINES:
            write_wrapped_lines(field['description'], out)
        else:
            for line in field['description'].splitlines():
                if len(line) == 0:
                    out.write('\n')
                    continue
                out.write('   ' + line + '\n')

    out.seek(0)

    with open(OUTPUT_FILENAME, 'w') as f_out:
        f_out.write(out.read())
