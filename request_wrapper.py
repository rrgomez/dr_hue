""" Simple module for wrapping the requests """

import re
import requests
import json
from urlparse  import urlparse
from constants import sanitize_error_messages
from constants import HTTP_DELETE, HTTP_GET, HTTP_HEAD, HTTP_OPTIONS, HTTP_POST, HTTP_PUT

HTTP_BASIC_AUTH  = "HTTPBasicAuth"
HTTP_DIGEST_AUTH = "HTTPDigestAuth"
VALID_SCHEMES    = ['http', 'https']

BASEURL = "api/<username>"

class GenericCallMethodException(Exception):
    """ Exception class called when there is a generic failure that didn't involve a response from
    the server """
    def __init__(self, msg, **kwargs):
        super(GenericCallMethodException, self).__init__(msg, **kwargs)

class JsonRpcGetException(Exception):
    """ Exception class called when an API fails """
    def __init__(self, msg, rsp=None, keys=None, **kwargs):
        super(JsonRpcGetException, self).__init__(msg, **kwargs)
        self.rsp  = rsp
        self.keys = keys or {}

    
def _sanitize_url(url, variables):
    """ Quickly sanitize url """
    for key in variables:
        url = re.sub('<'+key+'>', variables[key], url)
    return url

def request_get(url):
    """ Make a simple get to a given url and return the response """
    parsed_url = urlparse(url)
    if parsed_url.scheme not in VALID_SCHEMES:
        msg = "No valid scheme found, please include one of '%s' in your url" % VALID_SCHEMES
        raise GenericCallMethodException(msg)

    # save the response and throw an error if the get didn't work
    response = requests.get(url)
    response.raise_for_status()
    return response

def json_rpc_call(url, method_type, method_name, params, keys, base_url_overide=None):
    """ API Call wrapper for accessing the Hue system

    :param str url: The url that has the api
    :param str method_type: they type of HTTP request to make
    :param str method_name: the method name you are calling
    :param dict params: the python payload for the call method
    :param dict keys: the keys associated with the method call

    :rtype: dict
    :Returns: the response to the API Call
    """

    # If method param is None, fail
    #if params.get('method', None) is None and not base_url_overide:
     #   raise GenericCallMethodException("No method parameter found!")

    # Cleanup the url
    base_url      = base_url_overide or "%s/%s/%s" % (url, BASEURL, method_name)
    qualified_url = _sanitize_url(base_url, keys)

    # If url doesn't have http or https, fail
    parsed_url = urlparse(qualified_url)
    if parsed_url.scheme not in VALID_SCHEMES and not base_url_overide :
        msg = "No valid scheme found, please include one of '%s' in your url" % VALID_SCHEMES
        raise GenericCallMethodException(msg)

    data = json.dumps(params)
    response = {
        HTTP_DELETE:  lambda x: requests.delete(qualified_url,  data=data),
        HTTP_GET:     lambda x: requests.get(qualified_url,     data=data),
        HTTP_HEAD:    lambda x: requests.head(qualified_url,    data=data),
        HTTP_OPTIONS: lambda x: requests.options(qualified_url, data=data),
        HTTP_POST:    lambda x: requests.post(qualified_url,    data=data),
        HTTP_PUT:     lambda x: requests.put(qualified_url,     data=data)
    }[method_type](None)

    response.raise_for_status()
    for rsp in response:
        if 'error' in rsp:
            msg = "api_failure: %s " % rsp["error"]["description"]
            raise JsonRpcGetException(msg, rsp=response, keys=keys)

    return response.json()