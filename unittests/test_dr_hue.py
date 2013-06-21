""" Test the new platform changes """

import unittest
import dr_hue
from time import sleep
from multiprocessing.pool import ThreadPool

# Supply your own values here
USERNAME = ""
DEVICE_TYPE = "dr-hue"
THREAD_MAX  = 10

class PhueyTests(unittest.TestCase):
    """ Unittests to test the phuey api wrappers """

    def setUp(self):
        # Find the bridge, assuming only 1 bridge
        bridge_ip = dr_hue.discover_local_bridges()[0]['internalipaddress']

        # Create user
        self.url = "http://{0}".format(bridge_ip)

        global USERNAME 
        if not USERNAME:
            response = dr_hue.create_user(self.url, DEVICE_TYPE)
            username = response[0]['success']['username']
            USERNAME = username

    def tearDown(self):
        pass

    def test_turn_lights_on_interval(self):
        """ Test to turn on all lights on with an interval, and then off """

        print "\n"
        print "****************************************************"
        print "Testing turning on all lights with 2 second interval"
        print "****************************************************"
        
        lights = {}

        # Find all the lights
        lights.update(dr_hue.get_all_lights(self.url, USERNAME))
        print "There are %s lights, turning them on one by one now" % len(lights)

        for light in lights.keys():
            dr_hue.turn_light_on(self.url, light, USERNAME) 
            sleep(2)

        print "Now turning %s lights off one by one" % len(lights)

        for light in lights.keys():
            dr_hue.turn_light_off(self.url, light, USERNAME)
            sleep(2)
    
    def test_turn_lights_on_same_time(self):
        """ Test to turn on all lights on at the same time, and then off at the same time """

        print "\n"
        print "****************************************************"
        print "Testing turning on all lights at the same time"
        print "****************************************************"

        # Find bridges to associate with
        lights = {}
        lights.update(dr_hue.get_all_lights(self.url, USERNAME))

        print "There are %s lights, turning them all on now" % len(lights)
        pool = ThreadPool(len(lights) or THREAD_MAX)

        for light in lights.keys():
            args = (self.url, light, USERNAME)
            pool.apply_async(dr_hue.turn_light_on, args=args)

        # Wait for all the threads to complete then make sure everything is Kosher
        pool.close()
        pool.join()

        print "Now trying to turn them all off at the same time in 5 seconds"
        pool = ThreadPool(len(lights) or THREAD_MAX)
        sleep(5)

        for light in lights.keys():
            args = (self.url, light, USERNAME)
            pool.apply_async(dr_hue.turn_light_off, args=args)

        # Wait for all the threads to complete then make sure everything is Kosher
        pool.close()
        pool.join()

################################################################################
# Setup Testcases to run
################################################################################

if __name__ == "__main__":
    unittest.main()