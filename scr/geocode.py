'''
$ python geocode.py [-u <username>] [-p <password>]

Get latitude and longitude for cities in the Spreadsheet by accessing
the Google Maps API.

Only runs queries for missing geocode data.
'''

# stdlib
import argparse
# local
from access import *


def geo_cell_target_map(client, schema):
    '''
    Create a map of Geocode columns to column indexes
    {
        'longitude': x,
        'latitude': y,
        'raw': z
    }
    '''
    prefix = schema['geo']['target']
    cells = client.GetCellsFeed(schema['gd_key'])

    header_cells = [entry.cell for entry in cells.entry
        if int(entry.cell.row) == 1
        and entry.cell.text.startswith(prefix)]

    header_map = dict()
    for cell in header_cells:
        if 'Lat' in cell.text:
            header_map['latitude'] = int(cell.col)
        elif 'Long' in cell.text:
            header_map['longitude'] = int(cell.col)
        elif 'Raw' in cell.text:
            header_map['raw'] = int(cell.col)

    return header_map

def location_string_factory(schema):
    '''
    Create a generator for location strings based on schema
    '''
    geo_cols = [clean_cell(h) for h in schema['geo']['location']]

    def location_string_gen(row):
        row_fields = row.custom
        loc = []

        for col in geo_cols:
            loc_part = row_fields[col].text
            if loc_part:
                loc.append(loc_part)

        loc_str = ', '.join(loc)

        return loc_str

    return location_string_gen

def has_geocode_data(row):
    '''
    Check whether row has geocode data
    '''
    row_data = row.custom
    clean_prefix = clean_cell(schema['geo']['target'])
    headers = [clean_cell(key) for key in schema['col_map'].keys()]
    geo_cells = [bool(row_data[h].text)
        for h in headers if h.startswith(clean_prefix)]

    return sum(geo_cells) == len(geo_cells)

def cell_updater_factory(client, key):
    '''
    Create a cell updater for a spreadsheet
    '''
    def updater(row, col, inputValue):
        client.UpdateCell(
            row=row,
            col=col,
            inputValue=inputValue,
            key=key
        )
    return updater

def update_geocode(row, row_num, loc_gen, geo_cells, updater):
    '''
    Update the geocode data in the given row of the spreadsheet
    specified by the key.
    '''
    loc_str = loc_gen(row)
    geocode_raw = GoogleIntegration.geocode(loc_str, 'json')
    
    # XXX: should handle error response
    geo_json = json.loads(geocode_raw)['results'][0]

    location = geo_json['geometry']['location']
    latitude = location['lat']
    longitude = location['lng']

    # update Geocode - Raw
    updater(row_num, geo_cells['raw'], geocode_raw)

    # update Geocode - Lat
    updater(row_num, geo_cells['latitude'], str(latitude))

    # update Geocode - Long
    updater(row_num, geo_cells['longitude'], str(longitude))


def update_missing_geocodes(client, schema):
    '''
    Get missing geocodes for locations in sheet 
    '''
    key = schema['gd_key']
    rows = client.GetListFeed(key).entry
    geo_cells = geo_cell_target_map(client, schema)
    loc_gen = location_string_factory(schema)
    updater = cell_updater_factory(client, key)

    for i, row in enumerate(rows):
        row_num = i + 2

        if not has_geocode_data(row):
            print >>stderr, "Getting geo data for %s ... " \
                % row.custom['city'].text
            update_geocode(row, row_num, loc_gen, geo_cells, updater)


if __name__=='__main__':
    # Parse args 
    parser = argparse.ArgumentParser(
        description='Geocode data in the spreadsheet'
    )
    setup_access_cli(parser)
    args = parser.parse_args()

    # set up access
    client = GoogleIntegration(
        args.user,
        args.password,
        'spreadsheet').connect()

    schema = parse_schema('schema.json')

    # browse spreadsheet for missing geocodes, fill them in
    update_missing_geocodes(client, schema)
