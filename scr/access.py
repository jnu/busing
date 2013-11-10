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
import re
import json
import argparse
import urllib
import urllib2
# 3rd party
import gdata.spreadsheet.service
import gdata.docs.service


# Helpers
def setup_access_cli(parser):
    '''
    Add username and password command line options
    '''
    parser.add_argument('-u', '--user', type=str,
        help="Google User Name")
    parser.add_argument('-p', '--password', type=str,
        help="Google Password")

def clean_cell(text):
    '''
    Strip text in the way Google does in the Data API for column headers
    '''
    return re.sub(r'[^\w\d\-_\.]', '', text).lower()

def parse_schema(fn):
    '''
    Parse a JSON schema given by file named `fn`
    '''
    schema = None
    with open(fn, 'r') as fh:
        schema = json.loads(fh.read())
    return schema


# Classes
class GoogleIntegration(object):
    '''
    Implement access to Google Spreadsheets, Data, and Maps APIs
    As far as necessary for the related scripts
    '''

    SERVICES = {
        'docs' : gdata.docs.service.DocsService,
        'spreadsheet' : gdata.spreadsheet.service.SpreadsheetsService
    }

    GEOCODE_URL = "http://maps.googleapis.com/maps/api/geocode/%s?sensor=false&address=%s"

    def __init__(self, username=None, password=None, service='docs'):
        self.username = username
        self.password = password
        self._ensure_auth_info()

        self.service = self.SERVICES[service]
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
        '''
        Login to Google Data API
        '''
        self.client.ClientLogin(self.username, self.password,
            source="Urban Busing Project")
        return self.client

    @classmethod
    def geocode(cls, location, output='json'):
        '''
        Access Google Maps API for information about `location`
        '''
        clean_loc = urllib.quote(location)
        url = cls.GEOCODE_URL % (output, clean_loc)

        uh = urllib2.urlopen(url)

        resp = uh.read()

        return resp


# Test
if __name__=='__main__':
    # Parse args 
    parser = argparse.ArgumentParser(description='Compile data from spreadsheet')
    setup_access_cli(parser)
    args = parser.parse_args()

    client = GoogleIntegration(args.user, args.password, 'spreadsheet').connect()
