#!/usr/bin/env python
import json

import yaml

MENU_FILENAME = '../config/satnogsconfig/menu.yml'
JSONMENU_FILENAME = 'config/menu-new.json'
OUTPUT_FILENAME = 'config/specs/development-new.json'

TYPE_MAP = {
    'integer': 'integer',
    'port': 'integer',
    'float': 'number',
    'boolean': 'boolean',
    'host': 'string',
    'url': 'string',
    'path': 'string',
    'string': 'string'
}

if __name__ == '__main__':
    with open(JSONMENU_FILENAME, 'r') as fjson:
        fields = json.load(fjson)

    with open(MENU_FILENAME) as f:
        menu = yaml.safe_load(f)

    properties = {}
    types = set()
    for name, field in fields.items():
        types.update([])

        json_type = TYPE_MAP[field['type']]
        properties.update({
            name.lower(): {
                'description': field.get('short_description', ''),
                'type': json_type,
            }
        })

    with open(OUTPUT_FILENAME, 'w') as fout:
        json.dump(properties, fout, indent=2)
        fout.write('\n')
