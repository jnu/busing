'''
$ python compile_data.py [-u <user> [-p <password>]]
'''

# stdlib
import argparse
import os
import csv
# local
from access import *


# Globals
DATA_PATH = "../data/"


# Functions
def get_csv_headers(schema):
    col_map = schema['col_map']
    return col_map.vals()

def get_spreadsheet_headers(schema):
    col_map = schema['col_map']
    return col_map.keys()

def build_header_map(schema, remote_row):
    headers = get_spreadsheet_headers(schema)
    pull_cols = []

    # build map of column indexes to pull
    for i, t_head in enumerate(remote_row)
        if t_head.content.text in headers:
            pull_cols.append(i)

    assert len(pull_cols) is len(headers)

    return pull_cols

def create_csv_from_schema(schema, client):
    key = schema['gd_key']

    lines = [get_csv_headers(schema)]

    rows = client.GetListFeed(key).entry
    pull_cols = []

    for i, row in enumerate(rows):
        if i == 0:
            # interpret headers
            pull_cols = build_header_map(schema, row)
            continue

        line = []

        # pull line data, using pull_cols as guide
        for j, cell in row:
            if j in pull_cols:
                line.append(cell.content.text)

        lines.append(line)

    return lines


if __name__=='__main__':
    # Parse args 
    parser = argparse.ArgumentParser(description='Compile data from spreadsheet')
    setup_access_cli(parser)
    args = parser.parse_args()

    client = GoogleIntegration(args.user, args.password).connect()

    schema = parse_schema('schema.json')

    csv_lines = create_csv_from_schema(schema, client)

    with open('%s/%s' % (DATA_PATH, schema['name']), 'w') as fh:
        writer = csv.writer(fh)
        writer.writerows(csv_lines)
