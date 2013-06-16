""" Python Library for calling the Hue API """

from constants import HTTP_DELETE, HTTP_GET, HTTP_POST, HTTP_PUT, PORTAL_URL
from request_wrapper import json_rpc_call, request_get

#########################################################################################################
# Lights API                                                                                            #
#########################################################################################################

def get_all_lights(url, username):
    """ Gets a list of all lights that have been discovered by the bridge.

    URL /api/<username>/lights
    Method  GET
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system
    :rtype: dict
    :Returns:
        Returns a list of all lights in the system, each light has a name and unique identification
        number. If there are no lights in the system then the bridge will return an empty object, {}.

        [
            "1": {
                "name": "Bedroom"
            },
            "2": {
                "name": "Kitchen"
            }
        ]
    """

    method_name = 'lights'
    keys        = {'username':username}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def get_light_attr(url, light_id, username):
    """ Gets the attributes and state of a given light.

        URL /api/<username>/lights/<id>
        Method  GET
        Version 1.0
        Permission  Whitelist

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system
    :param int light_id: the id of the light you wish to get attributes for

    :rtype: dict
    :Returns:

        State     object   Details the state of the light, see the state table below for more details.
        Type        string  A fixed name describing the type of light e.g. "Extended color light".
        name        string  A unique, editable name given to the light. (length 0 to 32)
        modelid     string  The hardware model of the light. (length 6)
        swversion   string  An identifier for the software version running on the light. (length 8)
        Pointsymbol object  This parameter is reserved for future functionality.

        State Object Properties:
            On    bool     On/Off state of the light. On=true, Off=false

            Bri   uint8    Brightness of the light. This is a scale from the minimum brightness the light
                           is capable of, 0, to the maximum capable brightness, 255. Note a brightness of
                           0 is not off.

            Hue   uint16w  Hue of the light. This is a wrapping value between 0 and 65535. Both 0 and
                           65535 are red, 25500 is green and 46920 is blue.

            sat   uint8    Saturation of the light. 255 is the most saturated (colored) and 0 is the
                           least saturated (white).

            xy    list     The x and y coordinates of a color in CIE color space. (2..2 of float 4)
                           The first entry is the x coordinate and the second entry is the y coordinate.
                           Both x and y are between 0 and 1.

            ct    uint16   The Mired Color temperature of the light. 2012 connected lights are capable of
                           153 (6500K) to 500 (2000K).

            alert str      The alert effect, which is a temporary change to the bulb's state. This can
                           take one of the following values:
                                "none"    - The light is not performing an alert effect.
                                "select"  - The light is performing one breathe cycle.
                                "lselect" - The light is performing breathe cycles for 30 seconds or
                                            until an "alert": "none" command is received.

                           Note that in version 1.0 this contains the last alert sent to the light and
                           not its current state. This will be changed to contain the current state in an
                           upcoming patch.

            effect  str    The dynamic effect of the light, can either be "none" or "colorloop".
                           If set to colorloop, the light will cycle through all hues using the current
                           brightness and saturation settings.

            colormode str  Indicates the color mode in which the light is working, this is the last
                           command type it received. Values are "hs" for Hue and Saturation, "xy" for
                           XY and "ct" for Color Temperature. This parameter is only present when the
                           light supports at least one of the values. (length 2)

            reachable bool Indicates if a light can be reached by the bridge. Currently always returns
                           true, functionality will be added in a future patch.

        {
            "state": {
                "hue": 50000,
                "on": true,
                "effect": "none",
                "alert": "none",
                "bri": 200,
                "sat": 200,
                "ct": 500,
                "xy": [0.5, 0.5],
                "reachable": true,
                "colormode": "hs"
            },
            "type": "Living Colors",
            "name": "LC 1",
            "modelid": "LC0015",
            "swversion": "1.0.3",
            "pointsymbol": {
                "1": "none",
                "2": "none",
                "3": "none",
                "4": "none",
                "5": "none",
                "6": "none",
                "7": "none",
                "8": "none"
            }
        }
    """

    method_name = 'lights/<id>'
    keys        = {'username':username, 'id': light_id}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def get_new_lights(url, username):
    """ Gets a list of lights that were discovered the last time a search for new lights was performed.
    The list of new lights is always deleted when a new search is started.

    URL /api/<username>/lights/new
    Method  GET
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:
        {
            "7": {"name": "Hue Lamp 7"},
            "8": {"name": "Hue Lamp 8"},
            "lastscan": "2012-10-29T12:00:00"
        }
    """

    method_name   = 'lights/new'
    keys        = {'username':username}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def rename_light(url, light_id, light_name, username):
    """ Used to rename lights. A light can have its name changed when in any state, including when it is
    unreachable or off.

    URL /api/<username>/lights/<id>
    Method  GET
    Version 1.0
    Permission  Whitelist

    Example request: {"name":"Bedroom Light"}

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system
    :param int light_id : the id of the light you wish to rename
    :param str light_name: The new name for the light. If the name is already taken a space and number
                           will be appended by the bridge e.g. "Bedroom Light 1".
    :rtype: dict
    :returns:
        [{"success":{"/lights/1/name":"Bedroom Light"}}]
    """

    method_name = 'lights/<id>'
    keys        = {'username': username, 'id': light_id}
    params      = {'name': light_name}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def search_for_new_lights(url, username):
    """ Starts a search for new lights.

    The bridge will search for 1 minute and will add a maximum of 15 new lights. To add further lights,
    the command needs to be sent again after the search has completed. If a search is already active, it
    will be aborted and a new search will start.

    When the search has finished, new lights will be available using the get new lights command. In
    addition, the new lights will now be available by calling get all lights or by calling get group
    attributes on group 0. Group 0 is a special group that cannot be deleted and will always contain all
    lights known by the bridge.

        URL /api/<username>/lights
        Method  POST
        Version 1.0
        Permission  Whitelist

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system

    :rtype: dict
    :Returns:
        Contains a list with a single item that details whether the search started successfully.
        [ { "success": { "/lights": "Searching for new devices" } } ]
    """

    method_name = 'lights'
    keys        = {'username':username}
    params      = {}

    return json_rpc_call(url, HTTP_POST, method_name, params, keys)

def set_light_state(url, light_id, username, params):
    """ Allows the user to turn the light on and off, modify the hue and effects.

    URL /api/<username>/lights/<id>/state
    Method  PUT
    Version 1.0
    Permission  Whitelist

        request example:
        {
            "hue": 50000,
            "on": true,
            "bri": 200
        }

    :param str url: The url of the Hue system
    :param int lgiht_id: the id of the light you wish to change the state on
    :param str username: the username that has access to the hue system
    :param dict params: the parameters you wish to use to change the state

    :returns:
        A response to a successful PUT request contains confirmation of the arguments passed in.

        Note: If the new value is too large to return in the response due to internal memory
        constraints then a value of "Updated." is returned.

        [
            {"success":{"/lights/1/state/bri":200}},
            {"success":{"/lights/1/state/on":true}},
            {"success":{"/lights/1/state/hue":50000}}
        ]
    """

    method_name = 'lights/<id>/state'
    keys        = {'username':username, 'id': light_id}

    return json_rpc_call(url, HTTP_PUT, method_name, params, keys)

#########################################################################################################
# Groups API                                                                                            #
#########################################################################################################

def get_all_groups(url, username):
    """ Gets a list of all groups that have been added to the bridge. A group is a list of lights that
    can be created, modified and deleted by a user. The maximum numbers of groups is 16. N.B. For the
    first bridge firmware release, bridge software version 01003542 only, a limited number of these APIs
    are supported in the firmware so only control of groups/0 is supported.

    Note:   Group 0 is a special group containing all lights in the system, and is not returned by the
            'get all groups' command.

    URL  /api/<username>/groups
    Method  GET
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:
        Returns a list of all groups in the system, each group has a name and unique identification number.
        If there are no groups then the bridge will return an empty object, {}.

        {
            "1": {
                "name": "Group 1"
            },
            "2": {
                "name": "VRC 2"
            }
        }
    """

    method_name = 'groups'
    keys        = {'username':username}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def create_group(url, username):
    """ Create Group: To be added in the future """
    print "create_group call not implemented in 1.0 release (%s, %s)" % (url, username)

def delete_group(url, username, group_id):
    """ Delete Group: To be added in the future """
    print "delete_group call not implemented in 1.0 release (%s, %s, %s)" % (url, username, group_id)

def get_group_attributes(url, group_id, username):
    """ Gets the name, light membership and last command for a given group.
            Note: Scenes are not used in the version of the API

    URL /api/<username>/groups/<id>
    Method  GET
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param int group_id: the id of the group you wish to get attributes for
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:

        action  object  The last command that was sent to the whole group.
                        Note this is not necessarily the current state of the group.
        lights  list    The IDs of the lights that are in the group.
        name    string  A unique, editable name given to the group. (length 0 to 32)

        {
            "action": {
                "on": true,
                "hue": 0,
                "effect": "none",
                "bri": 100,
                "sat": 100,
                "ct": 500,
                "xy": [0.5, 0.5]
            },
            "lights": [
                "1",
                "2"
            ],
            "name": "bedroom",
            "scenes": {
            }
        }
    """

    method_name = 'groups/<id>'
    keys        = {'username':username, 'id': group_id}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def set_group_attributes(url, group_id, username, params):
    """ Allows the user to modify the name and light membership of a group.

    URL /api/<username>/groups/<id>
    Method  PUT
    Version 1.0
    Permission  Whitelist

    Request example:

        {"name":"Bedroom","lights":["1"]}

    :param str url: The url of the Hue system
    :param int group_id: the id of the group you wish to set attributes for
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns: A response to a successful PUT request contains confirmation of the arguments passed in.

        Note: If the new value is too large to return in the response due to internal memory constraints
              then a value of "Updated." is returned.

        objects:
        name    string  The new name for the group. If the name is already taken a space and number will
                        be appended by the bridge e.g. "Custom Group 1".   (Length 0 to 32)
        lights  list    The IDs of the lights that should be in the group. This resource must contain an
                        array of at least one element. If an invalid light ID is given, error 7 will be
                        returned and the group not created.

        [
            {"success":{"/groups/1/lights":["1"]}},
            {"success":{"/groups/1/name":"Bedroom"}}
        ]

    """

    method_name = 'groups/<id>'
    keys        = {'username': username, 'id': group_id}

    return json_rpc_call(url, HTTP_PUT, method_name, params, keys)

def set_group_state(url, group_id, username, params):
    """ Modifies the state of all lights in a group. User created groups will have an ID of 1 or higher;
    however a special group with an ID of 0 also exists containing all the lamps known by the bridge.

    NOTES: A light cannot have its hue, saturation, brightness, effect, ct or xy modified when it is
    turned off. Doing so will return error 201. There are 3 methods available to set the color of the
    light - hue and saturation (hs), xy or color temperature (ct). If multiple methods are used then a
    priority is used: xy > ct > hs. All included parameters will be updated but the 'colormode' will be
    set using the priority system.

    URL /api/<username>/groups/<id>
    Method  PUT
    Version 1.0
    Permission  Whitelist

    State Object Properties:
        On    bool     On/Off state of the light. On=true, Off=false

        Bri   uint8    Brightness of the light. This is a scale from the minimum brightness the light
                       is capable of, 0, to the maximum capable brightness, 255. Note a brightness of
                       0 is not off.

        Hue   uint16w  Hue of the light. This is a wrapping value between 0 and 65535. Both 0 and
                       65535 are red, 25500 is green and 46920 is blue.

        sat   uint8    Saturation of the light. 255 is the most saturated (colored) and 0 is the
                       least saturated (white).

        xy    list     The x and y coordinates of a color in CIE color space. (2..2 of float 4)
                       The first entry is the x coordinate and the second entry is the y coordinate.
                       Both x and y are between 0 and 1.

        ct    uint16   The Mired Color temperature of the light. 2012 connected lights are capable of
                       153 (6500K) to 500 (2000K).

        alert str      The alert effect, which is a temporary change to the bulb's state. This can
                       take one of the following values:
                            "none"    - The light is not performing an alert effect.
                            "select"  - The light is performing one breathe cycle.
                            "lselect" - The light is performing breathe cycles for 30 seconds or
                                        until an "alert": "none" command is received.

                       Note that in version 1.0 this contains the last alert sent to the light and
                       not its current state. This will be changed to contain the current state in an
                       upcoming patch.

        effect  str    The dynamic effect of the light, can either be "none" or "colorloop".
                       If set to colorloop, the light will cycle through all hues using the current
                       brightness and saturation settings.

        colormode str  Indicates the color mode in which the light is working, this is the last
                       command type it received. Values are "hs" for Hue and Saturation, "xy" for
                       XY and "ct" for Color Temperature. This parameter is only present when the
                       light supports at least one of the values. (length 2)

        reachable bool Indicates if a light can be reached by the bridge. Currently always returns
                       true, functionality will be added in a future patch.

    Example Request:
        {
            "on": true,
            "hue": 2000,
            "effect": "colorloop"
        }

    :param str url: The url of the Hue system
    :param int group_id: the id of the group you wish to set a particular state for
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns: A response to a successful PUT request contains confirmation of the arguments passed in.

              Note: If the new value is too large to return in the response due to internal memory
                    constraints then a value of "Updated." is returned.

        [
            {"success":{"/groups/1/action/on": true}},
            {"success":{"/groups/1/action/effect":"colorloop"}},
            {"success":{"/groups/1/action/hue":6000}}
        ]

    """

    method_name = 'groups/<id>'
    keys        = {'username': username, 'id': group_id}

    return json_rpc_call(url, HTTP_PUT, method_name, params, keys)

#########################################################################################################
# Schedules API                                                                                         #
#########################################################################################################

def create_scehdule(url, username, params):
    """ Allows the user to create new schedules. The bridge can store up to 100 schedules.

    URL /api/<username>/schedules
    Method  POST
    Version 1.0
    Permission  Whitelist

    Request object uses only these variables:

        name        str  Name for the new schedule. If a name is not specified then the default name,
                         "schedule", is used. If the name is already taken a space and number will be
                         appended by the bridge, e.g. "schedule 1" (length 0 to 32)
        description str  Description of the new schedule. If the description is not specified it will be
                         empty.  (lenght 0 to 64)
        command     obj  Command to execute when the scheduled event occurs. If the command is not valid
                         then an error of type 7 will be raised. Tip: Stripping unnecessary whitespace
                         can help to keep commands within the 90 character limit.
        time        str  Time when the scheduled event will occur in ISO 8601:2004 format. The bridge
                         measures time in UTC and only accepts extended format, non-recurring, local
                         time (YYYY-MM-DDThh:mm:ss). Incorrectly formatted dates will raise an error of
                         type 7. If the time is in the past an error 7 will also be raised.

    Request example:
        {
            "name": "Wake up",
            "description": "My wake up alarm",
            "command": {
                "address": "/api/0/groups/1/action",
                "method": "PUT",
                "body": {
                    "on": true
                }
            },
            "time": "2011-03-30T14:24:40"
        }

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system
    :param dict params: the parameter dictionary for scheduling

    :rtype: dict
    :returns: Contains a list with a single item that details whether the schedule was added
              successfully.

        [{
            "success":{"id": "2"}
        }]

    """

    method_name = 'schedules'
    keys        = {'username': username}

    return json_rpc_call(url, HTTP_POST, method_name, params, keys)

def delete_schedule(url, schedule_id, username):
    """ Deletes a schedule from the bridge.

    URL /api/<username>/schedules/<id>
    Method  DELETE
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param int schedule_id: the schedule you wish to delete
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns: The response details whether the schedule was successfully deleted.
        [
            {"success": "/schedules/1 deleted."}
        ]
    """

    method_name = 'schedules/<id>'
    keys        = {'username': username, 'id': schedule_id}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def get_all_schedules(url, username):
    """ Gets a list of all schedules that have been added to the bridge.

    URL /api/<username>/schedules
    Method  GET
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns: Returns a list of all schedules in the system. Each group has a name and unique
              identification number. If there are no schedules then the bridge will return an empty
              object, {}.
        {
          "1":{
              "name":"Wake up"
          },
          "2":{
              "name":"Sleep down"
          }
        }

    """

    method_name = 'schedules'
    keys        = {'username': username}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def get_schedule_attributes(url, schedule_id, username):
    """ Gets all attributes for a schedule.

    URL /api/<username>/schedules/<id>
    Method  GET
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param int schedule_id: the id of the schedule you are querying
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:
        name        str  Name for the new schedule. If a name is not specified then the default name,
                         "schedule", is used. If the name is already taken a space and number will be
                         appended by the bridge, e.g. "schedule 1" (length 0 to 32)
        description str  Description of the new schedule. If the description is not specified it will be
                         empty.  (lenght 0 to 64)
        command     obj  Command to execute when the scheduled event occurs. If the command is not valid
                         then an error of type 7 will be raised. Tip: Stripping unnecessary whitespace
                         can help to keep commands within the 90 character limit.
        time        str  Time when the scheduled event will occur in ISO 8601:2004 format. The bridge
                         measures time in UTC and only accepts extended format, non-recurring, local
                         time (YYYY-MM-DDThh:mm:ss). Incorrectly formatted dates will raise an error of
                         type 7. If the time is in the past an error 7 will also be raised.
    """


    method_name = 'schedules/<id>'
    keys        = {'username': username, 'id': schedule_id}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def set_scehdule_attributes(url, schedule_id, username, params):
    """ Allows the user to change attributes of a schedule.

    URL /api/<username>/schedules/<id>
    Method  PUT
    Version 1.0
    Permission  Whitelist

    Request object uses only these variables:

    name        str  Name for the new schedule. If a name is not specified then the default name,
                     "schedule", is used. If the name is already taken a space and number will be
                     appended by the bridge, e.g. "schedule 1" (length 0 to 32)
    description str  Description of the new schedule. If the description is not specified it will be
                     empty.  (lenght 0 to 64)
    command     obj  Command to execute when the scheduled event occurs. If the command is not valid
                     then an error of type 7 will be raised. Tip: Stripping unnecessary whitespace
                     can help to keep commands within the 90 character limit.
    time        str  Time when the scheduled event will occur in ISO 8601:2004 format. The bridge
                     measures time in UTC and only accepts extended format, non-recurring, local
                     time (YYYY-MM-DDThh:mm:ss). Incorrectly formatted dates will raise an error of
                     type 7. If the time is in the past an error 7 will also be raised.

    Request example:
        {
            "name": "Wake up"
        }

    :param str url: The url of the Hue system
    :param int schedule_id: the schedule you wish to set attributes for
    :param str username: the username that has access to the hue system
    :param dict params: the parameter dictionary for scheduling

    :rtype: dict
    :returns: A response to a successful PUT request contains confirmation of the arguments passed in.
              Note: If the new value is too large to return in the response due to internal memory
              constraints then a value of "Updated." is returned.

        [
            { "success": {"/schedules/1/name": "Wake up"}}
        ]

    """
    method_name = 'schedules/<id>'
    keys        = {'username': username, 'id': schedule_id}

    return json_rpc_call(url, HTTP_PUT, method_name, params, keys)

#########################################################################################################
# Configuration API                                                                                     #
#########################################################################################################

def create_user(url, device_type):
    """ Creates a new user. The link button on the bridge must be pressed and this command executed
    within 30 seconds. Once a new user has been created, the user key is added to a 'whitelist',
    allowing access to API commands that require a whitelisted user. At present, all other API commands
    require a whitelisted user.

    NOTE: We ask that published apps use the name of their app as the devicetype.

    URL /api
    Method  POST
    Version 1.0
    Permission  All

    Request example:
        {"devicetype": "iPhone", "username": "1234567890"}

    :param str devicetype: Description of the type of device associated with this username. This field
                           must contain the name of your app (length 0 to 40)
    :param str username  : A username. If this is not provided, a random key will be generated and
                           returned in the response. It is recommended that a unique identifier for the
                           device be used as the username
    :rtype: dict
    :returns: Contains a list with a single item that details whether the user was added successfully
              along with the username parameter.

              Note: If the requested username already exists then the response will report a success.

    [{"success":{"username": "1234567890"}}]
    """

    base_url = "%s/api" %url
    method_name = "api"
    keys        = {'devicetype': device_type}
    params      = {'devicetype': device_type}

    return json_rpc_call(url, HTTP_POST, method_name, params, keys, base_url_overide=base_url)

def delete_user_from_whitelist(url, username, user_to_delete):
    """ Deletes the specified user, <user_to_delete>, from the whitelist.

    URL /api/<username>/config/whitelist/<username2>
    Method  DELETE
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system

    :rtype: dictionary
    :returns:
        The response details whether the user was successfully removed from the whitelist.

        [{
            "success": "/config/whitelist/1234567890 deleted."
        }]

    """

    method_name = "config/whitelist/<user_to_delete>"
    keys        = {'username': username, 'user_to_delete': user_to_delete}
    params      = {}

    return json_rpc_call(url, HTTP_DELETE, method_name, params, keys)

def get_configuration(url, username):
    """ Returns list of all configuration elements in the bridge. Note all times are stored in UTC.

    URL /api/<username>/config
    Method  GET
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:
        proxyport      int  Port of the proxy being used by the bridge. If set to 0 then a proxy is not
                            being used.
        utc            str  Current time stored on the bridge.
        name           str  Name of the bridge. This is also its uPnP name, so will reflect the actual
                            uPnP name after any conflicts have been resolved. (length 4 to 16)
        swupdate       obj  Contains information related to software updates.
        whitelist      list An array of whitelisted user IDs.
        swversion      str  Software version of the bridge.
        proxyaddress   str  IP Address of the proxy server being used. A value of "none" indicates no
                            proxy (length 0 to 40)
        mac            str  MAC address of the bridge.
        linkbutton     bool Indicates whether the link button has been pressed within the last 30
                            seconds.
        ipaddress      str  IP address of the bridge.
        netmask        str  Network mask of the bridge.
        gateway        str  Gateway IP address of the bridge.
        dhcp           bool Whether the IP address of the bridge is obtained with DHCP.
        portalservices bool This indicates whether the bridge is registered to synchronize data with a
                            portal account.

        {
            "proxyport": 0,
            "utc": "2012-10-29T12:00:00",
            "name": "Smartbridge 1",
            "swupdate": {
                "updatestate":1,
                 "url": "www.meethue.com/patchnotes/1453",
                 "text": "This is a software update",
                 "notify": false
             },
            "whitelist": {
                "1234567890": {
                    "last use date": "2010-10-17T01:23:20",
                    "create date": "2010-10-17T01:23:20",
                    "name": "iPhone Web 1"
                }
            },
            "swversion": "01003542",
            "proxyaddress": "none",
            "mac": "00:17:88:00:00:00",
            "linkbutton": false,
            "ipaddress": "192.168.1.100",
            "netmask": "255.255.0.0",
            "gateway": "192.168.0.1",
            "dhcp": false
        }

    """

    method_name = "config"
    keys        = {'username': username}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys)

def get_full_state(url, username):
    """ This command is used to fetch the entire datastore from the device, including settings and state
    information for lights, groups, schedules and configuration. It should only be used sparingly as it
    is resource intensive for the bridge, but is supplied e.g. for synchronization purposes.

    URL /api/<username>
    Method  GET
    Version 1.0
    Permission  Whitelist

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:
        lights    object  A collection of all lights and their attributes.
        groups    object  A collection of all groups and their attributes.
        config    object  All configuration settings.
        schedules object  A collection of all schedules and their attributes.

    """

    base_url    = 'api/<username>'
    method_name = ""
    keys        = {'username': username}
    params      = {}

    return json_rpc_call(url, HTTP_GET, method_name, params, keys, base_url_overide=base_url)

def modify_configuration(url, username, params):
    """ Allows the user to set some configuration values.

    URL /api/<username>/config
    Method  PUT
    Version 1.0
    Permission  Whitelist

    Parameter dictionary options:
        proxyport      int  Port of the proxy being used by the bridge. If set to 0 then a proxy is not
                            being used.
        utc            str  Current time stored on the bridge.
        name           str  Name of the bridge. This is also its uPnP name, so will reflect the actual
                            uPnP name after any conflicts have been resolved. (length 4 to 16)
        swupdate       obj  Contains information related to software updates.
        whitelist      list An array of whitelisted user IDs.
        swversion      str  Software version of the bridge.
        proxyaddress   str  IP Address of the proxy server being used. A value of "none" indicates no
                            proxy (length 0 to 40)
        mac            str  MAC address of the bridge.
        linkbutton     bool Indicates whether the link button has been pressed within the last 30
                            seconds.
        ipaddress      str  IP address of the bridge.
        netmask        str  Network mask of the bridge.
        gateway        str  Gateway IP address of the bridge.
        dhcp           bool Whether the IP address of the bridge is obtained with DHCP.
        portalservices bool This indicates whether the bridge is registered to synchronize data with a
                            portal account.

    Request example:
        {"proxyport":100}

    :param str url: The url of the Hue system
    :param str username: the username that has access to the hue system
    :param dict params: the parameter dictionary containing the configuration values you want to modify

    :rtype: dict
    :returns:

        [
            {"success": {"/config/proxyport":100}}
        ]

    """

    method_name = 'config'
    keys        = {'username': username}

    return json_rpc_call(url, HTTP_PUT, method_name, params, keys)

#########################################################################################################
# Portal API                                                                                            #
#########################################################################################################

def discover_local_bridges():
    """ This will enable you to discover the local IP your bridge has been assigned on your network.

        URL www.meethue.com/api/nupnp
        Method  GET
        Version 1.0 
        Permission  Open

        :rtype: list
        :returns: Returns a list of all bridges on the local network and their internal IP addresses. If
                  there are no bridges on your external IP then the system will return an empty list, [].

            [
                {
                    "id":"001788fffe0923cb",
                    "internalipaddress":"192.168.1.37",
                    "macaddress":"00:17:88:09:23:cb"
                }
            ]
    """

    return request_get(PORTAL_URL).json()

#########################################################################################################
# Composed and granular methods                                                                         #
#########################################################################################################

def get_username():
    """ Helper method to authenticate """
    bridge_ip = discover_local_bridges()[0]['internalipaddress']
    
    url = "http://{0}".format(bridge_ip)
    device_type = "dr-hue"
    response = create_user(url, device_type)
    
    return response[0]['success']['username']

def turn_all_lights_on(url, username, sleep_interval=0):
    """ All inclusive method that will get a user name, find all lights, turn on all lights"""
    from time import sleep 

    lights = {}
    lights.update(get_all_lights(url, username))

    print "Turning %s lights on one by one with interval of '%s' seconds" % (len(lights), sleep_interval)
    for light in lights.keys():
        turn_light_on(url, light, username)
        sleep(sleep_interval)

def turn_all_lights_off(url, username, sleep_interval=0):
    """ All inclusive method that will get a user name, find all lights, turn off all lights"""
    from time import sleep 

    lights = {}
    lights.update(get_all_lights(url, username))

    print "Turning %s lights off one by one with interval of '%s' seconds" % (len(lights), sleep_interval)
    for light in lights.keys():
        turn_light_off(url, light, username)
        sleep(sleep_interval)

def turn_light_off(url, light_id, username):
    """ Turn the light off

    :param str url: The url of the Hue system
    :param int light_id: the id of the light you wish to turn off
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:
            [ {"success":{"/lights/1/state/on":false}} ]
    """

    params = { "on": False }
    return set_light_state(url, light_id, username, params)

def turn_light_on(url, light_id, username):
    """ Turn the light on

    :param str url: The url of the Hue system
    :param int light_id: the id of the light you wish to turn on
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:
            [ {"success":{"/lights/1/state/on":true}} ]
    """

    params = { "on": True }
    return set_light_state(url, light_id, username, params)

def set_light_brightness(url, light_id, username, brightness):
    """ Set the brightness of an individual light

    :param str url: The url of the Hue system
    :param int light_id: the id of the light you wish to set brightness on
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:
            [ {"success":{"/lights/1/state/bri":200}} ]

    """

    params = { "bri": brightness }
    return set_light_state(url, light_id, username, params)

def set_light_hue(url, light_id, username, hue):
    """ Set the hue of an individual light

    :param str url: The url of the Hue system
    :param int light_id: the id of the light you wish to set hue on
    :param str username: the username that has access to the hue system

    :rtype: dict
    :returns:
            [ {"success":{"/lights/1/state/hue":50000}} ]

    """

    params = { "hue": hue }
    return set_light_state(url, light_id, username, params)