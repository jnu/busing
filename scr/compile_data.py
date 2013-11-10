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
    '''
    Get the titles to be used as CSV headers per schema
    '''
    col_map = schema['col_map']
    return col_map.values()

def get_spreadsheet_headers(schema):
    '''
    Get which headers are desired per schema
    '''
    col_map = schema['col_map']
    return col_map.keys()

def clean_headers(schema):
    '''
    Get headers that will match what Google names them in the ListFeed
    '''
    headers = get_spreadsheet_headers(schema)
    return [clean_cell(h) for h in headers]

def create_csv_from_schema(schema, client):
    '''
    Create a list of CSV rows from the Spreadsheet based on schema,
    connecting through client
    '''
    key = schema['gd_key']

    lines = [get_csv_headers(schema)]

    rows = client.GetListFeed(key).entry
    headers = clean_headers(schema)

    for i, row in enumerate(rows):
        line = []

        for header in headers:
            line.append(row.custom[header].text)

        lines.append(line)

    return lines


if __name__=='__main__':
    # Parse args 
    parser = argparse.ArgumentParser(description='Compile data from spreadsheet')
    setup_access_cli(parser)
    args = parser.parse_args()

    # set up access
    client = GoogleIntegration(args.user, args.password, 'spreadsheet').connect()

    schema = parse_schema('schema.json')

    # create CSV from spreadsheet per schema
    csv_lines = create_csv_from_schema(schema, client)

    # make sure paths exist
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    # save CSV locally
    path = ('%s/%s' % (DATA_PATH, schema['name'])).replace('//', '/')
    with open(path, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerows(csv_lines)
