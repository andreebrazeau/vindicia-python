import os
import inspect
import types
from vindicia.resource import *


"""

Vindicia's Python client library is an interface to its SOAP API.

Please see the Vindicia API documentation for more information:

"""

__version__ = '0.0.5'

USER = None
"""The SOAP api client user to authenticated against."""

PASSWORD = None
"""The SOAP api password user to authenticated with."""

VERSION = None
"""The SOAP api version used."""

ENVIRONMENT = None
"""The SOAP api environment to used. Production, Stage or Prodtest"""

DEFAULT_CURRENCY = 'USD'
"""The currency to use creating `Money` instances when one is not specified."""

SOCKET_TIMEOUT_SECONDS = None
"""The number of seconds after which to timeout requests to the Vindicia API.
If unspecified, the global default timeout is used."""


VIN_SOAP_HOST = None


VIN_HOA_HOST = "https://secure.{}vindicia.com/vws"

VIN_SOAP_WSDL_PATH = os.path.join(os.path.dirname(__file__), 'wsdl')


def get_soap_host():
    environement = vindicia.ENVIRONMENT
    if environement == "Production":
        vindicia.VIN_SOAP_HOST = "https://soap.vindicia.com"
    else:
        vindicia.VIN_SOAP_HOST = "https://soap.{}.sj.vindicia.com".format(environement)

"""
This should be enabled when I figure out about serialization of objects in some of the methods such as Transaction.score
which takes a transaction object.

class SoapDecorator(object):
    def __init__(self, f):
        self.f = f
        self.__name__ = self.f.__name__
        self.__doc__ = self.f.__doc__

        self.f_name = self.underscore_to_camelcase(self.f.__name__)

        inspection = inspect.getargspec(f)
        self.positional_arg_map = [
            self.underscore_to_camelcase(arg) for arg in inspection.args[1:]
        ]

        self.keyword_arg_map = {
            arg: self.underscore_to_camelcase(arg) for arg in inspection.args[1:]
        }

    def __call__(self, *args, **kwargs):
        params = {
            'parameters': {
                'auth': get_authentication(),
            }
        }

        # We only use this to validate that arguments are okay
        self.f(*args, **kwargs)

        # Add all positional arguments
        for idx, arg in enumerate(args[1:]):
            params['parameters'][self.positional_arg_map[idx]] = arg

        # Add all keyword arguments
        for k, v in kwargs:
            if v is not None:
                params['parameters'][self.keyword_arg_map[k]] = v

        return CallClient().call(args[0].__class__.__name__, self.f_name, params)

    def __get__(self, obj, ownerClass=None):
        return types.MethodType(self, obj)

    @classmethod
    def underscore_to_camelcase(cls, value):
        def camelcase():
            yield str.lower
            while True:
                yield str.capitalize

        c = camelcase()
        return "".join(c.next()(x) if x else '_' for x in value.split("_"))

"""


class SoapDecorator(object):
    """
    The does a lot of the common work so functions really only have to handle serializing the parameters they know about
    """
    def __init__(self, f):
        self.f = f
        self.__name__ = self.f.__name__
        self.__doc__ = self.f.__doc__

        self.f_name = self.underscore_to_camelcase(self.f.__name__)

    def __call__(self, *args, **kwargs):
        params = {
            'parameters': {
                'auth': get_authentication(),
            }
        }
        params['parameters'].update(self.f(*args, **kwargs))

        return CallClient().call(args[0].__class__.__name__, self.f_name, params)

    def __get__(self, obj, ownerClass=None):
        return types.MethodType(self, obj)

    @classmethod
    def underscore_to_camelcase(cls, value):
        def camelcase():
            yield str.lower
            while True:
                yield str.capitalize

        c = camelcase()
        return "".join(c.next()(x) if x else '_' for x in value.split("_"))


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
    _list_attr = {'4.3': [
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
    ],
    '8.0': [
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
        "statementFormat",
        "statementFormat",
        "invoiceTerms",
        "statementOffset",
        "statementTemplateId",
        "billingPlanCampaignCode",
        "billingPlanCampaignId",
        "billingPlanHistory",
    ],}

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

    def fetch_by_account(self, account=None, includeChildren=None):
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

    def fetch_by_merchant_account_id(self, merchant_account_id=None, includeChildren=None):
        auth = get_authentication()

        call_params = {
            'auth': auth,
            'account': {'merchantAccountId': merchant_account_id},
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


class Transaction(BaseWSDL):
    _list_attr = [
        "VID",
        "amount",
        "originalAmount",
        "currency",
        "divisionNumber",
        "merchantTransactionId",
        "previousMerchantTransactionId",
        "timestamp",
        "account",
        "sourcePaymentMethod",
        "destPaymentMethod",
        "ecpTransactionType",
        "statusLog",
        "paymentProcessor",
        "sourcePhoneNumber",
        "shippingAddress",
        "nameValues",
        "transactionItems",
        "merchantAffiliateId",
        "merchantAffiliateSubId",
        "userAgent",
        "note",
        "preferredNotificationLanguage",
        "sourceMacAddress",
        "sourceIp",
        "billingStatementIdentifier",
        "taxExemptions",
        "salesTaxAddress",
        "verificationCode",
        "autoBillCycle",
        "billingPlanCycle",
    ]

    @SoapDecorator
    def fetch_by_vid(self, vid):
        raise NotImplementedError

    @SoapDecorator
    def fetch_by_web_session_vid(self, vid):
        raise NotImplementedError

    @SoapDecorator
    def fetch_by_merchant_transaction_id(self, merchant_transaction_id):
        raise NotImplementedError

    @SoapDecorator
    def fetch_delta_since(self, timestamp, end_timestamp, page=None, page_size=None, payment_method=None):
        params = {
            'timestamp': timestamp,
            'endTimestamp': end_timestamp,
        }
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if payment_method is not None:
            params['paymentMethod'] = payment_method

        return params

    @SoapDecorator
    def fetch_delta(self, page_size):
        raise NotImplementedError

    @SoapDecorator
    def fetch_by_autobill(self, autobill):
        raise NotImplementedError

    @SoapDecorator
    def fetch_by_payment_method(self, payment_method, page, page_size):
        raise NotImplementedError

    @SoapDecorator
    def auth(self, transaction, min_chargeback_probability, send_email_notification=None, campaign_code=None,
             dryrun=False):
        raise NotImplementedError

    @SoapDecorator
    def calculate_sales_tax(self, transaction):
        raise NotImplementedError

    @SoapDecorator
    def capture(self, transactions):
        raise NotImplementedError

    @SoapDecorator
    def cancel(self, transactions):
        raise NotImplementedError

    @SoapDecorator
    def auth_capture(self, transaction, send_email_notification=None, ignore_avs_policy=None, ignore_cvn_policy=None,
                     campaign_code=None, dryrun=None):
        raise NotImplementedError

    @SoapDecorator
    def report(self, transactions):
        raise NotImplementedError

    @SoapDecorator
    def score(self, transaction):
        raise NotImplementedError

    @SoapDecorator
    def finalize_pay_pal_auth(self, pay_pal_transaction_id, success):
        raise NotImplementedError

    @SoapDecorator
    def finalize_boku_auth_capture(self, transaction_vid, success):
        raise NotImplementedError

    @SoapDecorator
    def finalize_customer_action(self, transaction_vid):
        raise NotImplementedError

    @SoapDecorator
    def address_and_sales_tax_from_pay_pal_order(self, pay_pal_transaction_id):
        raise NotImplementedError

    @SoapDecorator
    def migrate(self, migration_transactions):
        raise NotImplementedError
