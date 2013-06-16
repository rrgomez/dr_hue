""" This is where all the library constants will live """

import re

HTTP_DELETE  = "DELETE"
HTTP_GET     = "GET"
HTTP_HEAD    = "HEAD"
HTTP_OPTIONS = "OPTIONS"
HTTP_POST    = "POST"
HTTP_PUT     = "PUT"
PORTAL_URL   = "http://www.meethue.com/api/nupnp"

# These are the general error responses for the HUE devices, these are taken from
#   http://developers.meethue.com/8_errormessages.html
HUE_ERRORS = {
    1   : 'Unauthorized user',
    2   : 'Body contains invalid JSON',
    3   : 'Resource, <resource>, not available',
    4   : 'Method, <method_name>, not available for resource, <resource>',
    5   : 'Missing parameters in body',
    6   : 'Parameter, <parameter>, not available',
    7   : 'Invalid value, <value>, for parameter, <parameter>',
    8   : 'Parameter, <parameter>, is not modifiable',
    901 : 'Internal error, <error code>',
    101 : 'Link button not pressed',
    201 : 'Parameter, <parameter>, is not modifiable. Device is set to off.',
    301 : 'Group could not be created. Group table is full.',
    302 : 'Device, <id>, could not be added to group. Device\'s group table is full.'
}

def sanitize_error_messages(response_dict, keys):
    """ Helper method to sanitize the error messages above and put in the proper values """
    error_type = int(response_dict['error']['type'])
    error_msg  = HUE_ERRORS[error_type]

    for key in keys:
        error_msg = re.sub('<'+key+'>', keys[key], error_msg)

    return error_msg