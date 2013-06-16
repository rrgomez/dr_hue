==========
dr_hue
==========

Phillips Hue control library based on the API found at http://developers.meethue.com/

Sample Usage:

    # Of course, the dr_hue folder needs to be in your python path, then you can import
    # and use the following sample. Be sure to press the link button on the bridge
    # before running this script.

    import dr_hue

    # Grabs the first bridge that is recognized
    bridge_ip = dr_hue.discover_local_bridges()[0]['internalipaddress']
    url       = "http://{0}".format(bridge_ip)
    username  = dr_hue.get_username()
    dr_hue.turn_all_lights_on(url, username, sleep_interval=2)
    dr_hue.turn_all_lights_off(url, username, sleep_interval=0)

Good luck commanding dr_hue!