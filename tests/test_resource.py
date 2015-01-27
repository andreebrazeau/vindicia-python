"""
To use
- USER=<user> PASSWORD=<pw> VIN_CLIENT_ENVIRONMENT=prodtest nosetest
"""

import unittest
import uuid
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


    def get_account(self, new=False):
        if new:
            uuid = "unitest-{}".format(uuid.uuid4())
            self.account = {
                'merchant_account_id': uuid,
                'email': "{}@test.com".formmat(uuid),
                'name': "Test Account"
            }
        else:
            self.account = {
                'merchant_account_id': "unittestaccount",
                'email': "unittestaccount@test.com",
                'name': "Test Account"
            }

        rsp = self.vin.Account(merchantAccountId=self.account['merchant_account_id'],
                     emailAdress=self.account['email'],
                     name=self.account['name']).update()
        self.assertTrue(rsp.get('completed'))
        vin_account=rsp['data'].account
        return vin_account

    def get_autobill(self, merchant_account_id, product, billing_plan, new=False):
        if new:
            self.autobill= {
                'billing_plan': 'pro_monthly',
                'account': {"merchantAccountId": merchant_account_id},
                'currency': "USD",
                'items': {"product": {'merchantProductId': "bitcasa_pro"}},
            }




