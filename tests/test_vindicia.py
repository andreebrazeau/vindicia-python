# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import uuid
from xml.etree import ElementTree
import mock
import unittest
from tests.test_resource import VindiciaTest


class VindiciaTestCase(VindiciaTest):

    def test_hello(self):
        import vindicia

    def test_Account(self):
        import vindicia
        name = "Andrée Brazeau"
        email = "test@test.test"
        user_id = 123
        lang = "fr"

        account = vindicia.Account(merchantAccountId=user_id, emailAddress=email, preferredLanguage=lang, name=name)

        self.assertIsNotNone(account)
        self.assertEqual(account.name, name)
        self.assertEqual(account.emailAddress, email)
        self.assertEqual(account.merchantAccountId, user_id)
        self.assertEqual(account.preferredLanguage, lang)
        self.assertIsInstance(account.to_dict(), dict)

    def test_Authentication(self):
        auth = self.vin.get_authentication()
        #import ipdb;ipdb.set_trace()

        self.assertIsNotNone(auth)
        print auth
        self.assertEqual(auth['version'], self.vin.VERSION)
        self.assertEqual(auth['login'], self.vin.USER)
        self.assertEqual(auth['password'], self.vin.PASSWORD)

    def test_BaseWsdl_to_dict(self):
        user_id = datetime.now()
        nv = self.vin.NameValuePair(name='Name', value="Value")
        # import ipdb;ipdb.set_trace()
        account = self.vin.Account(merchantAccountId=user_id, nameValues=nv.to_dict())
        print account
        response = account.update()
        print response

        self.assertIsNotNone(response)
        self.assertTrue(response.get('completed'))

    def test_account_update(self):
        name = "Wayne Gretzky"
        email = "test@test.test"
        user_id = 123
        lang = "fr"

        account = self.vin.Account(merchantAccountId=user_id, emailAddress=email, preferredLanguage=lang, name=name)

        response = account.update()
        self.assertIsNotNone(response)
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['data'].account.merchantAccountId, str(user_id))

    def test_account_fetch_by_merchant_account_id_good(self):
        good_user_id = 123
        account = self.vin.Account()

        response = account.fetch_by_merchant_account_id(good_user_id)

        self.assertIsNotNone(response)
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['data'].account.merchantAccountId, str(good_user_id))

    def test_account_fetch_by_merchant_account_id_bad(self):
        bad_user_id = "none_existant_id"
        account = self.vin.Account()

        response = account.fetch_by_merchant_account_id(bad_user_id)

        self.assertFalse(response.get('completed'))
        self.assertEqual(response['return_code'], 400)

    def test_account_update_payment_method(self):
        account = self.vin.Account(merchantAccountId=123)
        pm = self.vin.PaymentMethod(
            type="MerchantAcceptedPayment",
            merchantAcceptedPayment={
                "paymentType": "iTunes",
            },
            merchantPaymentMethodId=123,
        )

        response = account.update_payment_method(pm.to_dict())
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)

    def test_billing_plan(self):

        rate_plan = self.vin.BillingPlan()
        response = rate_plan.fetch_all()
        #import ipdb;ipdb.set_trace()
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)

    def test_name_value_pair(self):
        name = "this_is_a_name"
        value = "this_is_the_value"
        nvp = self.vin.NameValuePair(name=name, value=value)

        self.assertIsNotNone(nvp)
        self.assertEqual(nvp.name, name)
        self.assertEqual(nvp.value, value)

    def test_web_session(self):
        method = "AutoBill_update"
        ip = "10.0.0.0"
        return_url = "http://bit.com/success"
        error_url = "http://bit.com/error"
        version = self.vin.VERSION

        web_session = self.vin.WebSession(method=method,
                                       ipAddress=ip,
                                       returnURL=return_url,
                                       errorURL=error_url,
                                       version=version,
                                       )

        self.assertIsNotNone(web_session)
        self.assertEqual(web_session.method, method)
        self.assertEqual(web_session.ipAddress, ip)
        self.assertEqual(web_session.returnURL, return_url)
        self.assertEqual(web_session.errorURL, error_url)
        self.assertIsNotNone(web_session.version)


    def test_set_private_form_value(self):
        name = "name1"
        value = "value1"

        method = "AutoBill_update"
        ip = "10.0.0.0"
        return_url = "http://bit.com/success"
        error_url = "http://bit.com/error"
        name2 = "name2"
        value2 = "value2"

        nv1 = self.vin.NameValuePair(name=name, value=value)
        nv2 = self.vin.NameValuePair(name=name2, value=value2)

        web_session = self.vin.WebSession(method=method,
                                          ipAddress=ip,
                                          returnURL=return_url,
                                          errorURL=error_url,
                                          privateFormValues=[nv1.to_dict(), nv2.to_dict()])

        self.assertIsNotNone(web_session.privateFormValues)
        self.assertEqual(len(web_session.privateFormValues), 2)


    def test_set_methodParamValues(self):
        name = "name1"
        value = "value1"

        method = "AutoBill_update"
        ip = "10.0.0.0"
        return_url = "http://bit.com/success"
        error_url = "http://bit.com/error"

        nv1 = self.vin.NameValuePair(name=name, value=value)

        web_session = self.vin.WebSession(method=method,
                                          ipAddress=ip,
                                          returnURL=return_url,
                                          errorURL=error_url,
                                          methodParamValues=nv1
                                          )


        self.assertIsNotNone(web_session.methodParamValues)

    def test_websession_initialize(self):

        method = "AutoBill_update"
        ip = "10.0.0.0"
        return_url = "http://bit.com/success"
        error_url = "http://bit.com/error"

        web_session = self.vin.WebSession(method=method,
                                          ipAddress=ip,
                                          returnURL=return_url,
                                          errorURL=error_url)

        #import ipdb;ipdb.set_trace()
        response = web_session.initialize()
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)

    def test_websession_initialize_with_method_param_value(self):

        method = "AutoBill_update"
        ip = "10.0.0.0"
        return_url = "http://bit.com/success"
        error_url = "http://bit.com/error"
        good_user_id = 123
        nv1 = self.vin.NameValuePair(name="vin_Account_merchantAccountId", value=good_user_id)
        nv2 = self.vin.NameValuePair(name="vin_AutoBill_sourceIp", value=ip)
        web_session = self.vin.WebSession(method=method,
                                          ipAddress=ip,
                                          returnURL=return_url,
                                          errorURL=error_url,
                                          privateFormValues=[nv1.to_dict(), nv2.to_dict()]
        )

        #import ipdb;ipdb.set_trace()
        response = web_session.initialize()
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)

    def test_websession_finalize(self):
        # Get VID from a session
        method = "AutoBill_update"
        return_url = "http://bit.com/success"
        error_url = "http://bit.com/error"
        web_session = self.vin.WebSession(method=method,
                                          returnURL=return_url,
                                          errorURL=error_url)
        response = web_session.initialize()
        #import ipdb;ipdb.set_trace()
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)

    def test_websession_fetch_by_vid(self):
        # Get VID from a session
        method = "AutoBill_update"
        return_url = "http://bit.com/success"
        error_url = "http://bit.com/error"
        web_session = self.vin.WebSession(method=method,
                                          returnURL=return_url,
                                          errorURL=error_url)
        session = web_session.initialize()
        vid = session['data'].session.VID

        web_session = self.vin.WebSession()
        response = web_session.fetch_by_vid(vid)
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)

    def test_payment_method(self):
        VID = "123123"
        type = "type"
        accountHolderName = "test test"
        billingAddress = {
            "postalCode": 123123
        }
        payment_method = self.vin.PaymentMethod(VID=VID, type=type, accountHolderName=accountHolderName,
                                                billingAddress=billingAddress)
        self.assertIsNotNone(payment_method)
        self.assertEqual(payment_method.VID, VID)
        self.assertEqual(payment_method.type, type)
        self.assertEqual(payment_method.accountHolderName, accountHolderName)
        self.assertEqual(payment_method.billingAddress, billingAddress)

    def test_payment_method_update(self):
        VID = 123132
        payment_method = self.vin.PaymentMethod(VID=123132)
        response = payment_method.update(validate=False)

        self.assertIsNotNone(response)

    def test_payment_method_fetch_by_web_session_id(self):
        vid = 'f5e914526250d228cef1dae545978d3eaa6d46d9'
        payment_method = self.vin.PaymentMethod()
        response = payment_method.fetch_by_web_session_vid(vid)
        print response
        self.assertNotEqual(getattr(response['data'], 'return').returnCode, "500")

    def test_AutoBill(self):
        nextBilling = "123"
        account = {
            'VID': 465465
        }

        Auto_bill = self.vin.AutoBill(nextBilling=nextBilling, account=account)
        self.assertIsNotNone(Auto_bill)
        self.assertEqual(Auto_bill.nextBilling, nextBilling)
        self.assertEqual(Auto_bill.account, account)

    def test_AutoBill_update(self):
        billing_plan = {
            'merchantBillingPlanId': "premium_monthly"
        }
        items = [{'product': {'merchantProductId': 'bitcasa_premium'}}]

        auto_bill = self.vin.AutoBill()#billingPlan=billing_plan, items=items)
        response = auto_bill.update(campaignCode='supercool2')
        print response
        self.assertNotEqual(getattr(response['data'], 'return').returnCode, "500")

    def test_AutoBill_fetchByAccount(self):
        good_user_id = 123132
        other_good_user = 123
        account = self.vin.Account(merchantAccountId=other_good_user)
        auto_bill = self.vin.AutoBill()
        response = auto_bill.fetchByAccount(account=account)

        print response
        self.assertNotEqual(getattr(response['data'], 'return').returnCode, "500")

    def test_AutoBill_upgrade(self):
        account = self.vin.Account(merchantAccountId=123)
        auto_bill = self.vin.AutoBill()
        response = auto_bill.fetchByAccount(account=account)

        #import ipdb;ipdb.set_trace()
        print response
        self.assertNotEqual(getattr(response['data'], 'return').returnCode, "500")

    def test_Autobill_update_coupon_invalid(self):
        account = self.vin.Account(merchantAccountId=123)
        # import ipdb;ipdb.set_trace()
        autobill = self.vin.AutoBill(billingPlan={'merchantBillingPlanId': "pro_monthly"},
                                     account={"merchantAccountId": 123},
                                     currency="USD",
                                     items={"product": {'merchantProductId': "bitcasa_pro"}})
        response = autobill.update(validatePaymentMethod=False,
                                   dryrun=True,
                                   campaignCode="supercool2")

        self.assertIsNotNone(response)
        self.assertFalse(response.get('completed'))
        self.assertEqual(response['return_code'], 400)

    def test_Autobill_update_coupon_valid(self):

        autobill = self.vin.AutoBill(billingPlan={'merchantBillingPlanId': "premium_monthly"},
                                     account={"merchantAccountId": 123},
                                     currency="USD",
                                     items={"product": {'merchantProductId': "bitcasa_premium"}})
        response = autobill.update(validatePaymentMethod=False,
                                   dryrun=True,
                                   campaignCode="HALFOFF")

        self.assertIsNotNone(response)
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)

    def test_autobill_fetch_delta_since(self):
        autobill = self.vin.AutoBill()
        timestamp = datetime.utcnow() - timedelta(days=1)

        response = autobill.fetch_delta_since(timestamp)
        print response
        self.assertIsNotNone(response)
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)

    def test_account_make_payment(self):
        #create account
        created_account = self.vin.Account(
            merchantAccountId=123123,
            emailAddress='123123@test.com',
            preferredLanguage="ENG",
            name="Test Vindicia"
        )
        response = created_account.update()
        print response
        #create payment method
        merchantPaymentMethodId = uuid.uuid4().hex
        account = self.vin.Account(merchantAccountId=self.user.id)
        pm = self.vin.PaymentMethod(
            type="MerchantAcceptedPayment",
            merchantAcceptedPayment={
                "paymentType": "iTunes",
            },
            merchantPaymentMethodId=merchantPaymentMethodId,
        )
        response = account.update_payment_method(payment_method=pm.to_dict())
        print response

        #create Autobill
        data = {"purchase_date_pst": "2013-10-10 17:19:00 America/Los_Angeles",
                "expires_date": "1381451040000",
                "product_id": "com.Bitcasa.Bitcasa.infinite_month",
                "original_transaction_id": uuid.uuid4().hex,
                "unique_identifier": "408e8f478108ba73335bbebe62ecdd987f07165d",
                "original_purchase_date_pst": "2013-10-10 16:54:02 America/Los_Angeles",
                "expires_date_formatted_pst": "2013-10-10 17:24:00 America/Los_Angeles",
                "original_purchase_date": "2013-10-10 23:54:02 Etc/GMT",
                "expires_date_formatted": "2013-10-11 00:24:00 Etc/GMT",
                "bvrs": "211013",
                "original_purchase_date_ms": "1381449242000",
                "purchase_date": "2013-10-11 00:19:00 Etc/GMT",
                "web_order_line_item_id": "1000000027448157",
                "purchase_date_ms": "1381450740000",
                "item_id": "668648908",
                "bid": "com.Bitcasa.Bitcasa",
                "transaction_id": "1000000089744225",
                "quantity": "1"}
        plan_name = "premium_monthly_itunes"

        response = self.sync_apple_billing_in_vindicia(self.user.id, data, plan_name)
        print response

        autobill_id = response.autobill.merchantAutoBillId
        autobill = self.vin.AutoBill(merchantAutoBillId=autobill_id)

        import ipdb;ipdb.set_trace()
        merchantPaymentMethodId = uuid.uuid4().hex
        account = self.vin.Account(merchantAccountId=self.user.id)
        pm = self.vin.PaymentMethod(
            type="MerchantAcceptedPayment",
            merchantAcceptedPayment={
                "paymentType": "iTunes",
            },
            merchantPaymentMethodId=merchantPaymentMethodId,
        )
        response = account.update_payment_method(payment_method=pm.to_dict())
        import ipdb;ipdb.set_trace()
        print response

        response = autobill.make_payment(payment_method=pm.to_dict(),
                                         amount=99)
        print response

        self.assertIsNotNone(response)
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)

    def test_entitlement_fetchByAccount(self):
        autobill = self.vin.Entitlement()

        response = autobill.fetch_by_account(merchant_account_id=315457)
        print response
        self.assertIsNotNone(response)
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)
        self.assertIsNotNone(response['data'].entitlements)
        self.assertEqual(len(response['data'].entitlements), 1)

    def test_entitlement_fetchByAccount_none(self):
        autobill = self.vin.Entitlement()

        response = autobill.fetch_by_account(merchant_account_id=259057)
        print response
        self.assertIsNotNone(response)
        self.assertTrue(response.get('completed'))
        self.assertEqual(response['return_code'], 200)
        self.assertEqual(getattr(response['data'], 'entitlements', []), [])
