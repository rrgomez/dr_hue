""" Test the new platform changes """

import unittest
import hue_api
from time import sleep
from multiprocessing.pool import ThreadPool

# Supply your own values here
USERNAME = ""
DEVICE_TYPE = ""
BRIDGE_IP = "http://"
THREAD_MAX  = 10

class PhueyTests(unittest.TestCase):
    """ Unittests to test the phuey api wrappers """

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def off_test_turn_on_all_lights_with_interval(self):
        """ Test to turn on all lights on with an interval, and then off """

        print "\n"
        print "****************************************************"
        print "Testing turning on all lights with 2 second interval"
        print "****************************************************"

        # Find bridges to associate with
        #bridges = hue_api.discover_local_bridges()
        bridges = [BRIDGE_IP]
        
        lights = {}
        #for bridge in bridges:

            # Sanitize a url for api use
            
        # Create user
        #response = hue_api.create_user(url, DEVICE_TYPE)
        #username = response[0]['success']['username']

        # Find all the lights
        lights.update(hue_api.get_all_lights(BRIDGE_IP, USERNAME))
        print "There are %s lights, turning them on one by one now" % len(lights)

        for light in lights.keys():
            hue_api.turn_light_on(BRIDGE_IP, light, USERNAME) 
            sleep(2)

        print "Now turning %s lights off one by one" % len(lights)

        for light in lights.keys():
            hue_api.turn_light_off(BRIDGE_IP, light, USERNAME)
            sleep(2)
    
    def off_test_turn_on_all_lights_at_same_time(self):
        """ Test to turn on all lights on at the same time, and then off at the same time """

        print "\n"
        print "****************************************************"
        print "Testing turning on all lights at the same time"
        print "****************************************************"

        # Find bridges to associate with
        lights = {}
        lights.update(hue_api.get_all_lights(BRIDGE_IP, USERNAME))

        print "There are %s lights, turning them all on now" % len(lights)
        pool = ThreadPool(len(lights) or THREAD_MAX)

        for light in lights.keys():
            args = (BRIDGE_IP, light, USERNAME)
            pool.apply_async(hue_api.turn_light_on, args=args)

        # Wait for all the threads to complete then make sure everything is Kosher
        pool.close()
        pool.join()

        print "Now trying to turn them all off at the same time in 5 seconds"
        pool = ThreadPool(len(lights) or THREAD_MAX)
        sleep(5)

        for light in lights.keys():
            args = (BRIDGE_IP, light, USERNAME)
            pool.apply_async(hue_api.turn_light_off, args=args)

        # Wait for all the threads to complete then make sure everything is Kosher
        pool.close()
        pool.join()

    def test_turn_on_all_lights_and_adjust_color_with_interval(self):
        """ Test to turn on all lights on and then cycle through the colors with an interval, and then off """

        print "\n"
        print "****************************************************"
        print "Testing turning on all lights with 2 second interval"
        print "****************************************************"

        # Find bridges to associate with
        #bridges = hue_api.discover_local_bridges()
        bridges = [BRIDGE_IP]
        
        lights = {}
        #for bridge in bridges:

            # Sanitize a url for api use
            
        # Create user
        #response = hue_api.create_user(url, DEVICE_TYPE)
        #username = response[0]['success']['username']

        # Find all the lights
        lights.update(hue_api.get_all_lights(BRIDGE_IP, USERNAME))
        print "There are %s lights, turning them on one by one now" % len(lights)

  

        pool = ThreadPool(len(lights) or THREAD_MAX)

        for light in lights.keys():
            params = {"hue": 25000, "on":True, "bri":100, "effect":"colorloop"}
            args = (BRIDGE_IP, light, USERNAME, params)
            pool.apply_async(hue_api.set_light_state, args=args)

        # Wait for all the threads to complete then make sure everything is Kosher
        pool.close()
        


        #pool.join()

        #ool = ThreadPool(len(lights) or THREAD_MAX)
        #sleep(5)


        def hue_adjustment(url, light, username):
            for i in [i for i in range(0, 65536) if (i % 600 == 0)]:
                sleep(0.4)
                hue_api.set_light_hue(url, light, username, i)

     #   for light in lights.keys():
      #      args = (BRIDGE_IP, light, USERNAME)
       #     pool.apply_async(hue_adjustment, args=args)

        # Wait for all the threads to complete then make sure everything is Kosher
        #pool.close()
        #pool.join()


        #for light in lights.keys():
        #    hue_api.turn_light_on(BRIDGE_IP, light, USERNAME)             
        #    sleep(10)

 #       print "Now turning %s lights off one by one" % len(lights)

  #      for light in lights.keys():
    #        hue_api.turn_light_off(BRIDGE_IP, light, USERNAME)
   #         sleep(2)
    

################################################################################
# Setup Testcases to run
################################################################################

if __name__ == "__main__":
    unittest.main()