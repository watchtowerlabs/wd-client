#!/usr/bin/env python
import json
import yaml

MENU_FILENAME = '../config/satnogsconfig/menu.yml'
JSONMENU_FILENAME = 'config/menu.json'
OUTPUT_FILENAME = 'config/menu-new.json'


if __name__ == '__main__':
    with open(JSONMENU_FILENAME, 'r') as fjson:
        fields = json.load(fjson)

    with open(MENU_FILENAME) as f:
        menu = yaml.safe_load(f)

    new_fields = {}

    categories = menu['items']['Advanced']['items'].keys()
    for name, field in fields.items():
        for category in categories:
            try:
                entry = menu['items']['Advanced']['items'][category]['items'][name]
                field['input_method'] = entry['type']
                field['short_description'] = entry['short_description']
                field['init'] = entry['init']
                if 'categories' in field.keys():
                    # No support for multiple categories (yet?)
                    pass
                else:
                    field['categories'] = ['Advanced', category]
            except KeyError:
                pass

    with open(OUTPUT_FILENAME, 'w') as fout:
        json.dump(fields, fout, indent=2)
        fout.write('\n')
