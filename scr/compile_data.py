'''
$ python compile_data.py [-u <user> [-p <password>]]
'''

# stdlib
import argparse
import os
import csv
import re
# local
from access import *


# Globals
DATA_PATH = "../data/"
t = None

# Functions
def get_csv_headers(schema):
    col_map = schema['col_map']
    return col_map.values()

def get_spreadsheet_headers(schema):
    col_map = schema['col_map']
    return col_map.keys()

def clean_headers(schema):
    headers = get_spreadsheet_headers(schema)
    return [re.sub(r'[^\w\d\-_\.]', '', h).lower() for h in headers]

def create_csv_from_schema(schema, client):
    key = schema['gd_key']

    lines = [get_csv_headers(schema)]

    rows = client.GetListFeed(key).entry
    headers = clean_headers(schema)

    for i, row in enumerate(rows):
        line = []

        # pull line data, using pull_cols as guide
        for header in headers:
            line.append(row.custom[header].text)

        lines.append(line)

    return lines


if __name__=='__main__':
    # Parse args 
    parser = argparse.ArgumentParser(description='Compile data from spreadsheet')
    setup_access_cli(parser)
    args = parser.parse_args()

    client = GoogleIntegration(args.user, args.password, 'spreadsheet').connect()

    schema = parse_schema('schema.json')

    csv_lines = create_csv_from_schema(schema, client)

    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        
    path = ('%s/%s' % (DATA_PATH, schema['name'])).replace('//', '/')
    with open(path, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerows(csv_lines)
