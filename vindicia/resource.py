from datetime import datetime
from suds.client import Client
import logging
import os

import vindicia

#logging.basicConfig(level=logging.DEBUG)

#logging.getLogger('suds.client').setLevel(logging.DEBUG)


VIN_SOAP_TIMEOUT = 120


def get_authentication():
    return {
        'login': vindicia.VIN_SOAP_CLIENT_USER,
        'password': vindicia.VIN_SOAP_CLIENT_PASSWORD,
        'version': vindicia.VIN_SOAP_CLIENT_VERSION,
    }


class BaseWSDL(object):
    def __init__(self, vin_object=None,  **kwargs):
        if vin_object:
            for attr_name in self._list_attr:
                if getattr(vin_object, attr_name, None):
                    setattr(self, attr_name, getattr(vin_object, attr_name))
                else:
                    setattr(self, attr_name, None)
        else:
            for attr_name in self._list_attr:
                if kwargs.get(attr_name) is not None:
                    setattr(self, attr_name, kwargs[attr_name])
                else:
                    setattr(self, attr_name, None)

    def to_dict(self):
        attr_dict = {}
        for attrName in self._list_attr:
            attr_dict[attrName] = getattr(self, attrName)
        return attr_dict


class CallClient(object):
    def call(self, group, action, inputs):
        wsdl_file = 'file://%s/%s.wsdl' % (vindicia.VIN_SOAP_WSDL_PATH, group)
        return_data = {}
        try:
            client = Client(url=wsdl_file, location=vindicia.VIN_SOAP_HOST)
            call = getattr(client.service, action)
            response = call(**inputs['parameters'])
            if response:
                resp_return = getattr(response, 'return', None)
                if resp_return and getattr(resp_return, 'returnCode', None):
                    return_data['return_code'] = int(resp_return.returnCode)
                    return_data['return_string'] = resp_return.returnString
                    return_data['data'] = response
                    return_data['completed'] = True if resp_return.returnCode == '200' else False
                    return return_data
                else:
                    return_data['return_code'] = int(response.returnCode)
                    return_data['return_string'] = response.returnString
                    return_data['soap_id'] = response.soapId
                    return_data['data'] = response
                    return_data['completed'] = True if resp_return.returnCode == '200' else False
                    return return_data

        except Exception, exc:
            return_data['return_code'] = 499
            return_data['return_string'] = exc.message if exc.message != "" else "Undefined Error"
            return_data['completed'] = False
            return return_data


class Account(BaseWSDL):
    _list_attr = ['VID',
                  'merchantAccountId',
                  'emailAddress',
                  'emailTypePreference',
                  'preferredLanguage',
                  'warnBeforeAutobilling',
                  'company',
                  'name',
                  'shippingAddress',
                  'paymentMethods',
                  'nameValues',
                  'taxExemptions',
                  'tokenBalances',
                  'credit',
                  'entitlements',
                  ]

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)

    def update(self):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'account': self.to_dict()
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('Account', 'update', inputs)
        return ret

    def fetch_by_merchant_account_id(self, merchant_account_id):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'merchantAccountId': merchant_account_id
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('Account', 'fetchByMerchantAccountId', inputs)
        return ret

    def update_payment_method(self, payment_method, replace_on_all_auto_bills=False,
                              update_behavior='Update', ignore_avs_policy=False, ignore_cvn_policy=False):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'account': self.to_dict(),
            'paymentMethod': payment_method,
            'replaceOnAllAutoBills': replace_on_all_auto_bills,
            'updateBehavior': update_behavior,
            'ignoreAvsPolicy': ignore_avs_policy,
            'ignoreCvnPolicy': ignore_cvn_policy,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('Account', 'updatePaymentMethod', inputs)
        return ret

    def make_payment(self, payment_method, amount, currency="USD", invoice_id=None, overage_disposition=None, note=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'account': self.to_dict(),
            'paymentMethod': payment_method,
            'amount': amount,
            'currency': currency,
            'invoiceId': invoice_id,
            'overageDisposition': overage_disposition,
            'note': note,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()

        ret = soap.call('Account', 'makePayment', inputs)
        return ret



class BillingPlan(BaseWSDL):
    _list_attr = [
        'VID',
        'merchantBillingPlanId',
        'description',
        'status',
        'periods',
        'prenotifyDays',
        'endOfLifeTimestamp',
        'nameValues',
        'merchantEntitlementIds',
        'billingStatementIdentifier',
    ]

    def __init__(self, **kwargs):
        super(BillingPlan, self).__init__(**kwargs)

    def fetch_all(self):
        auth = get_authentication()

        call_params = {
            'auth': auth,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('BillingPlan', 'fetchAll', inputs)
        return ret


class WebSession(BaseWSDL):
    _list_attr = [
        "VID",
        "method",
        "version",
        "returnURL",
        "errorURL",
        "ipAddress",
        "expireTime",
        "nameValues",
        "postValues",
        "methodParamValues",
        "privateFormValues",
        "apiReturn",
        "apiReturnValues",
    ]

    def __init__(self, **kwargs):
        super(WebSession, self).__init__(**kwargs)

    def initialize(self):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'session': self.to_dict(),
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('WebSession', 'initialize', inputs)
        return ret

    def finalize(self):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'session': self.to_dict(),
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('WebSession', 'finalize', inputs)
        return ret

    def fetch_by_vid(self, vid):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'vid': vid,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('WebSession', 'fetchByVid', inputs)
        return ret


class NameValuePair(BaseWSDL):
    _list_attr = [
        "name",
        "value"
    ]

    def __init__(self, **kwargs):
        super(NameValuePair, self).__init__(**kwargs)


class PaymentMethod(BaseWSDL):
    _list_attr = [
        "VID",
        "type",
        "creditCard",
        "ecp",
        "directDebit",
        "paypal",
        "boleto",
        "hostedPage",
        "merchantAcceptedPayment",
        "carrierBilling",
        "nameValues",
        "accountHolderName",
        "billingAddress",
        "customerSpecifiedType",
        "customerDescription",
        "merchantPaymentMethodId",
        "currency",
        "sortOrder",
        "active",
    ]

    def __init__(self, **kwargs):
        super(PaymentMethod, self).__init__(**kwargs)

    def update(self, validate=None, minChargebackProbability=None, replaceOnAllAutoBills=None, sourceIp=None,
               replaceOnAllChildAutoBills=None, ignoreAvsPolicy=None, ignoreCvnPolicy=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'paymentMethod': self.to_dict(),
            'validate': validate,
            'minChargebackProbability': minChargebackProbability,
            'replaceOnAllAutoBills': replaceOnAllAutoBills,
            'sourceIp': sourceIp,
            'replaceOnAllChildAutoBills': replaceOnAllChildAutoBills,
            'ignoreAvsPolicy': ignoreAvsPolicy,
            'ignoreCvnPolicy': ignoreCvnPolicy,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('PaymentMethod', 'update', inputs)
        return ret

    def fetch_by_web_session_vid(self, vid):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'vid': vid,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('PaymentMethod', 'fetchByWebSessionVid', inputs)
        return ret


class AutoBill(BaseWSDL):
    _list_attr = [
        "VID",
        "merchantAutoBillId",
        "account",
        "billingPlan",
        "paymentMethod",
        "currency",
        "customerAutoBillName",
        "status",
        "startTimestamp",
        "endTimestamp",
        "items",
        "sourceIp",
        "billingStatementIdentifier",
        "billingDay",
        "minimumCommitment",
        "merchantAffiliateId",
        "merchantAffiliateSubId",
        "warnOnExpiration",
        "nextBilling",
        "nameValues",
        "credit",
        "upgradedFromVid",
        "upgradedToVid",
        "statementFormat",
        "invoiceTerms",
        "statementOffset",
        "statementTemplateId",
        "billingPlanCampaignCode",
        "billingPlanCampaignId",
    ]

    def __init__(self, **kwargs):
        super(AutoBill, self).__init__(**kwargs)

    def update(self, duplicateBehavior=None, validatePaymentMethod=None, minChargebackProbability=None,
               ignoreAvsPolicy=None, ignoreCvnPolicy=None, campaignCode=None, dryrun=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'autobill': self.to_dict(),
            'duplicateBehavior': duplicateBehavior,
            'validatePaymentMethod': validatePaymentMethod,
            'minChargebackProbability': minChargebackProbability,
            'ignoreAvsPolicy': ignoreAvsPolicy,
            'ignoreCvnPolicy': ignoreCvnPolicy,
            'campaignCode': campaignCode,
            'dryrun': dryrun,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('AutoBill', 'update', inputs)
        return ret

    def addCapaign(self, product=None, item=None, applyToBillingPlan=None, capaignCode=None, dryrun=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'autobill': self.to_dict(),
            'product': product,
            'item': item,
            'applyToBillingPlan': applyToBillingPlan,
            'capaignCode': capaignCode,
            'dryrun': dryrun,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('AutoBill', 'update', inputs)
        return ret

    def fetchByAccount(self, account=None, includeChildren=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'account': account.to_dict(),
            'includeChildren': includeChildren,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('AutoBill', 'fetchByAccount', inputs)
        return ret

    def upgrade(self, skipOnetimeCharge=None, costLimit=None, effectiveDate=None, dryrun=None,
                negativeNet=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'autobill': self.to_dict(),
            'skipOnetimeCharge': skipOnetimeCharge,
            'costLimit': costLimit,
            'effectiveDate': effectiveDate,
            'dryrun': dryrun,
            'negativeNet': negativeNet,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('AutoBill', 'upgrade', inputs)
        return ret

    def cancel(self, disentitle=None, force=None, settle=None):

        auth = get_authentication()

        call_params = {
            'auth': auth,
            'autobill': self.to_dict(),
            'disentitle': disentitle,
            'force': force,
            'settle': settle,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()

        ret = soap.call('AutoBill', 'cancel', inputs)
        return ret

    def finalizePayPalAuth(self, payPalTransactionId, success):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'payPalTransactionId': payPalTransactionId,
            'success': success,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()

        ret = soap.call('AutoBill', 'finalizePayPalAuth', inputs)
        return ret

    def fetch_delta_since(self, timestamp, page=0, page_size=100, end_timestamp=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'timestamp': timestamp,
            'page': page,
            'pageSize': page_size,
            'endTimestamp': end_timestamp,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()

        ret = soap.call('AutoBill', 'fetchDeltaSince', inputs)
        return ret

    def fetch_by_merchant_auto_bill_id(self, merchant_auto_bill_id):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'merchantAutoBillId': merchant_auto_bill_id,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()

        ret = soap.call('AutoBill', 'fetchByMerchantAutoBillId', inputs)
        return ret


    def make_payment(self, payment_method, amount, currency="USD", invoice_id=None, overage_disposition=None, note=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'autobill': self.to_dict(),
            'paymentMethod': payment_method,
            'amount': amount,
            'currency': currency,
            'invoiceId': invoice_id,
            'overageDisposition': overage_disposition,
            'note': note,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()

        ret = soap.call('AutoBill', 'makePayment', inputs)
        return ret

class Entitlement(BaseWSDL):
    _list_attr = [
        "VID",
        "merchantEntitlementId",
        "description",
        "merchantAutoBillId",
        "autoBillVID",
        "merchantProductId",
        "productVID",
        "account",
        "startTimestamp",
        "endTimestamp",
        "active",
        "source",
    ]

    def __init__(self, **kwargs):
        super(Entitlement, self).__init__(**kwargs)

    def fetch_by_account(self, merchant_account_id, show_all=False, include_children=False):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'account': {'merchantAccountId': merchant_account_id},
            'showAll': show_all,
            'includeChildren': include_children,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()
        ret = soap.call('Entitlement', 'fetchByAccount', inputs)
        return ret

    def fetch_delta_since(self, timestamp, page=0, page_size=100, end_timestamp=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'timestamp': timestamp,
            'page': page,
            'pageSize': page_size,
            'endTimestamp': end_timestamp,
        }

        inputs = {
            'parameters': call_params
        }

        soap = CallClient()

        ret = soap.call('Entitlement', 'fetchDeltaSince', inputs)
        return ret
