"""
To use
- USER=<user> PASSWORD=<pw> VIN_CLIENT_ENVIRONMENT=prodtest nosetest
"""

import unittest
import os
from datetime import datetime
import logging


class VindiciaTest(unittest.TestCase):

    def setUp(self):
        import vindicia

        # Mock everything out unless we have an API key.
        vindicia.USER = os.environ['USER']
        vindicia.PASSWORD = os.environ['PASSWORD']
        self.test_id = datetime.now().strftime('%Y%m%d%H%M%S')

        # Update our endpoint if we have a different test host.
        vindicia.VERSION = os.environ['VERSION']
        vindicia.ENVIRONMENT = os.environ['ENVIRONMENT']

        self.vin = vindicia
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('vindicia').setLevel(logging.INFO)
        logging.getLogger('suds.client').setLevel(logging.INFO)