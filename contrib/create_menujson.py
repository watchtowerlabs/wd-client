#!/usr/bin/env python
import json
import sys
from pathlib import Path

USERGUIDE_FILENAME = './docs/environment_variables.rst'
JSONMENU_FILENAME = 'config/menu.json'


def tokenize(lines):
    buffer = []
    last_line = lines[0]
    for line in lines[1:]:
        if len(line) == 0:
            continue
        if line[0] == '~':
            # Found next title underline, assemble last field
            if len(buffer) == 0:
                # Buffer was not initialized yet, continue
                continue
            yield buffer
            buffer = []
            continue

        buffer.append(last_line)
        last_line = line

    buffer.append(last_line)
    yield buffer


def parse_fields(grouped_lines):
    fields = {}

    for ls in grouped_lines:
        if len(ls) == 1:
            continue

        field_name = ls[0]
        description = ' '.join(list(line.strip() for line in ls[5:]))

        required_str = ls[3][12:-1]
        if required_str == 'Yes':
            required = True
        elif required_str == 'No':
            required = False
        else:
            print(f'Syntax error when parsing: \n{ls}')
            sys.exit(-1)

        default_str = ls[2][11:-1]
        if default_str in ['None', 'False', 'True', 'Flowgraph-defined']:
            default = default_str
        else:
            default = default_str[1:-1]
        fields.update({
            field_name: {
                'type': ls[1][8:-1],
                'default': default,
                'required': required,
                'description': description,
            }
        })

    return fields


if __name__ == '__main__':
    userguide = Path(USERGUIDE_FILENAME).read_text()
    start_idx = userguide.find('Environment variables')
    lines = userguide[start_idx:].split('\n')[1:]

    grouped_lines = list(tokenize(lines))[:]
    fields = parse_fields(grouped_lines)

    with open(JSONMENU_FILENAME, 'w') as fjson:
        json.dump(fields, fjson, indent=2)
        fjson.write('\n')
