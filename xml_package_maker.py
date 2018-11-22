# coding: utf-8

import sys
import argparse
from spskit.frontdesk import execute_xpm


if __name__ == '__main__':
    # script, xml_path, acron, INTERATIVE, GENERATE_PMC = read_inputs(args)

    if len(sys.argv) == 1:
        print('Abrir formulario para escolher XML')
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('xml')
        parser.add_argument('acron', nargs='?')
        parser.add_argument('-auto', action="store_true", default=False)
        parser.add_argument('-pmc', action="store_true", default=False)

        inputs = parser.parse_args()
        result, outputs = execute_xpm(
            inputs.xml, configuration={}, acron=inputs.acron)
        if result is False:
            print('\n'.join(outputs))
        else:
            print(outputs)
