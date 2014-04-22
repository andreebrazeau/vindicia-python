from vindicia.errors import *
from vindicia.resource import *


"""

Vindicia's Python client library is an interface to its SOAP API.

Please see the Vindicia API documentation for more information:

"""

__version__ = '0.0.1'

CLIENT_USER = None
"""The SOAP api client user to authenticated against."""

CLIENT_PASSWORD = None
"""The SOAP api password user to authenticated with."""

CLIENT_VERSION = None
"""The SOAP api version used."""

CLIENT_ENVIRONMENT = None
"""The SOAP api environment to used. Production, Stage or Prodtest"""

DEFAULT_CURRENCY = 'USD'
"""The currency to use creating `Money` instances when one is not specified."""

SOCKET_TIMEOUT_SECONDS = None
"""The number of seconds after which to timeout requests to the Vindicia API.
If unspecified, the global default timeout is used."""

VIN_SOAP_HOST = "https://soap.vindicia.com"


VIN_HOA_HOST = "https://secure.vindicia.com/vws"

VIN_SOAP_WSDL_PATH = os.path.join(os.path.dirname(__file__), 'wsdl')
