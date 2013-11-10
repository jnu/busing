'''
$ python geocode.py [-u <username>] [-p <password>]
'''

# stdlib
import argparse
# local
from access import *


if __name__=='__main__':
    # Parse args 
    parser = argparse.ArgumentParser(
        description='Geocode data in the spreadsheet'
    )
    setup_access_cli(parser)
    args = parser.parse_args()

    client = GoogleIntegration(args.user, args.password).connect()

    schema = parse_schema('schema.json')
