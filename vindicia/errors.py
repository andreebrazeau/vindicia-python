from xml.etree import ElementTree
from pip.vendor import six


class ResponseError(Exception):

    """An error received from the Vindicia API in response to an HTTP
    request."""

    def __init__(self, response_xml):
        self.response_xml = response_xml

    @property
    def response_doc(self):
        """The XML document received from the service."""
        try:
            return self.__dict__['response_doc']
        except KeyError:
            self.__dict__['response_doc'] = ElementTree.fromstring(self.response_xml)
            return self.__dict__['response_doc']

    @property
    def symbol(self):
        """The machine-readable identifier for the error."""
        el = self.response_doc.find('symbol')
        if el is not None:
            return el.text

    @property
    def message(self):
        """The human-readable description of the error."""
        el = self.response_doc.find('description')
        if el is not None:
            return el.text

    @property
    def details(self):
        """A further human-readable elaboration on the error."""
        el = self.response_doc.find('details')
        if el is not None:
            return el.text

    @property
    def error(self):
        """A fall-back error message in the event no more specific
        error is given."""
        el = self.response_doc.find('error')
        if el is not None:
            return el.text

    def __str__(self):
        return six.text_type(self).encode('utf8')

    def __unicode__(self):
        symbol = self.symbol
        if symbol is None:
            return self.error
        details = self.details
        if details is not None:
            return six.u('%s: %s %s') % (symbol, self.message, details)
        return six.u('%s: %s') % (symbol, self.message)


class ClientError(ResponseError):
    """An error resulting from a problem in the client's request (that
    is, an error with an HTTP ``4xx`` status code)."""
    pass

class UnauthorizedError(ClientError):

    """An error for a missing or invalid API key (HTTP ``401 Unauthorized``)."""

    def __init__(self, response_xml):
        self.response_text = response_xml

    def __str__(self):
        return six.text_type(self).encode('utf-8')

    def __unicode__(self):
        return six.text_type(self.response_text)


error_classes = {
#     400: BadRequestError,
    401: UnauthorizedError,
#     402: PaymentRequiredError,
#     403: ForbiddenError,
#     404: NotFoundError,
#     406: NotAcceptableError,
#     412: PreconditionFailedError,
#     415: UnsupportedMediaTypeError,
#     422: ValidationError,
#     500: InternalServerError,
#     502: BadGatewayError,
#     503: ServiceUnavailableError,
# }


def error_class_for_http_status(status):
    """Return the appropriate `ResponseError` subclass for the given
    HTTP status code."""
    try:
        return error_classes[status]
    except KeyError:
        def new_status_error(xml_response):
            return UnexpectedStatusError(status, xml_response)
        return new_status_error


__all__ = [x.__name__ for x in error_classes.values()]
