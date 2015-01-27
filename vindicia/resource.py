from suds.client import Client

import vindicia

VIN_SOAP_TIMEOUT = 120


def get_authentication():
    return {
        'login': vindicia.USER,
        'password': vindicia.PASSWORD,
        'version': vindicia.VERSION,
    }

def get_list_attr(vin_object):
    if type(vin_object._list_attr) == dict:
        return vin_object._list_attr[str(vindicia.VERSION)]
    return vin_object._list_attr


class BaseWSDL(object):
    def __init__(self, vin_object=None,  **kwargs):
        list_attr = get_list_attr(self)
        if vin_object:
            for attr_name in list_attr:
                if getattr(vin_object, attr_name, None):
                    setattr(self, attr_name, getattr(vin_object, attr_name))
                else:
                    setattr(self, attr_name, None)
        else:
            for attr_name in list_attr:
                if kwargs.get(attr_name) is not None:
                    setattr(self, attr_name, kwargs[attr_name])
                else:
                    setattr(self, attr_name, None)

    def to_dict(self):
        attr_dict = {}
        for attrName in get_list_attr(self):
            attr_dict[attrName] = getattr(self, attrName)
        return attr_dict


class CallClient(object):
    def call(self, group, action, inputs):
        wsdl_file = 'file://%s/%s/%s.wsdl' % (vindicia.VIN_SOAP_WSDL_PATH, vindicia.VERSION, group)
        return_data = {}
        try:
            if not vindicia.VIN_SOAP_HOST:
                vindicia.get_soap_host()
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


