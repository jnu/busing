'''
$ python compile_data.py [-u <user> [-p <password>]]
'''

# stdlib
import argparse
from access import *


if __name__=='__main__':
    # Parse args 
    parser = argparse.ArgumentParser(description='Compile data from spreadsheet')
    setup_access_cli(parser)
    args = parser.parse_args()

    client = GoogleIntegration(args.user, args.password).connect()
