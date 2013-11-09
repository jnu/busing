'''
$ python access.py [-u <user> [-p <password>]]

Module for accessing Google APIs 

Get a Google Client by running

client = GoogleIntegration(user, password, service=<service>).connect()
'''

# stdlib
from sys import stderr, argv
from getpass import getpass
import os
import json
import argparse
# 3rd party
import gdata.spreadsheet.service
import gdata.docs.service


# Globals
keys = {
    'spreadsheet': "0AsnHpWihusbxdHY1NmpnZ2Q0bllNX3pXY2dFMVRFYWc"
}


# Helpers
def setup_access_cli(parser):
    parser.add_argument('-u', '--user', type=str,
        help="Google User Name")
    parser.add_argument('-p', '--password', type=str,
        help="Google Password")


# Classes
class GoogleIntegration(object):
    services = {
        'docs' : gdata.docs.service.DocsService,
        'spreadsheet' : gdata.spreadsheet.service.SpreadsheetsService
    }

    def __init__(self, username=None, password=None, service='docs'):
        self.username = username
        self.password = password
        self._ensure_auth_info()

        self.service = self.services[service]
        self.client = self.service()

    def _ensure_auth_info(self):
        # username / password checking and tidying up
        if not self.username:
            with open('config.json', 'r') as fh:
                config = json.loads(fh.read())
                if 'username' in config:
                    self.username = config['username']
                if 'password' in config:
                    self.password = config['password']

        if not self.password:
            self.password = getpass("Password> ")

        if not self.password or not self.username:
            raise ValueError("Need username and password")

        if '@' not in self.username:
            self.username += '@gmail.com'

    def connect(self):
        self.client.ClientLogin(self.username, self.password,
            source="Urban Busing Project")
        return self.client


# Test
if __name__=='__main__':
    # Parse args 
    parser = argparse.ArgumentParser(description='Compile data from spreadsheet')
    setup_access_cli(parser)
    args = parser.parse_args()

    client = GoogleIntegration(args.user, args.password, 'spreadsheet').connect()

    # Test connection
    cells = client.GetCellsFeed(keys['spreadsheet'])
    