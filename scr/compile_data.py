'''
$ python compile_data.py [-u <user> [-p <password>]]

If no username and password are entered, script looks for these values
in config.json in the working directory.
'''

# stdlib
from sys import stderr, argv
from getpass import getpass
import os
import json
import argparse
# 3rd party
import gdata.spreadsheet.service

# Globals
SPREADSHEET_KEY= "0AsnHpWihusbxdHY1NmpnZ2Q0bllNX3pXY2dFMVRFYWc"




if __name__=='__main__':
    # Parse args 
    parser = argparse.ArgumentParser(description='Compile data from spreadsheet')
    parser.add_argument('-u', '--user', type=str,
        help="Google User Name")
    parser.add_argument('-p', '--password', type=str,
        help="Google Password")

    args = parser.parse_args()

    username = args.user
    password = args.password

    if not username:
        try:
            with open('config.json', 'r') as fh:
                config = json.loads(fh.read())
                if 'username' in config:
                    username = config['username']
                if 'password' in config:
                    password = config['password']
        except Exception as e:
            print >>stderr, "Bad config file: ", str(e)
            print >>stderr, __doc__
            exit(1)

    # allow hidden password entry
    if not password:
        password = getpass("Password> ")

    # username and password should now be known
    if not username and not password:
        print >>stderr, "Need both username and password"
        print >>stderr, __doc__

    # append `gmail` domain to username if not present
    if '@' not in username:
        username += '@gmail.com'

    # connect to Google Service
    client = gdata.spreadsheet.service.SpreadsheetsService()
    print >>stderr, "Logging into Google as %s ..." % username
    client.ClientLogin(username, password)

    cells = client.GetCellsFeed(SPREADSHEET_KEY)

    
