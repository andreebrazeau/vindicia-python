import unittest
import os
from datetime import datetime
import logging


class VindiciaTest(unittest.TestCase):

    def setUp(self):
        import vindicia

        # Mock everything out unless we have an API key.
        try:
            client_user = os.environ['vindicia_user']
            client_password = os.environ['vindicia_password']
        except KeyError:
            # Mock everything out.
            vindicia.CLIENT_USER = 'apikey'
            vindicia.CLIENT_PASSWORD = 'password'
            self.test_id = 'mock'
        else:
            vindicia.CLIENT_USER = client_user
            vindicia.CLIENT_PASSWORD = client_password
            # self.mock_request = self.noop_mock_request
            # self.mock_sleep = self.noop_mock_sleep
            self.test_id = datetime.now().strftime('%Y%m%d%H%M%S')

        # Update our endpoint if we have a different test host.
        try:
            client_version = os.environ['VIN_CLIENT_VERSION']
        except KeyError:
            vindicia.CLIENT_VERSION = "4.3"
        else:
            vindicia.CLIENT_VERSION = client_version

        try:
            client_environment = os.environ['VIN_CLIENT_ENVIRONMENT']
        except KeyError:
            vindicia.CLIENT_ENVIRONMENT = "prodtest"
        else:
            vindicia.CLIENT_ENVIRONMENT = client_environment

        logging.basicConfig(level=logging.INFO)
        logging.getLogger('vindicia').setLevel(logging.DEBUG)