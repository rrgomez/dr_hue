""" Test the new platform changes """

import unittest
from datastore import *

MAX_LIGHTS=100

class DatastoreTests(unittest.TestCase):

    def setUp(self):
        setup_database()

    def tearDown(self):
        purge()

    def test_add_all_lights(self):
        """ Test to add all lights to database """

        lights = []
        for i in range(0, MAX_LIGHTS):
            lights.append({'name':'Light %s' % i, "base_id":"%s" % i})

        add_all_lights(lights)
        added_lights = get_lights()
        self.assertEquals(len(added_lights), MAX_LIGHTS)
        self.assertEquals(type(added_lights), dict)

    def test_storing_lights(self):
        """ Test storing lights """

        with self.assertRaises(Exception):
            add_light_to_group({'name':'Light 1','base_id':'1'}, 'Group 1')

        # Create groups
        group_one   = Group(name='Group 1')
        add_light_to_group({'name':'Light 1','base_id':'1'}, 'Group 1')

        group_two   = Group(name='Group 2')
        add_light_to_group({'name':'Light 2','base_id':'2'}, 'Group 2')
        add_light_to_group({'name':'Light 3','base_id':'3'}, 'Group 2')
        add_light_to_group({'name':'Light 4','base_id':'4'}, 'Group 2')
        add_light_to_group({'name':'Light 5','base_id':'5'}, 'Group 2')
        add_light_to_group({'name':'Light 6','base_id':'6'}, 'Group 2')
        add_light_to_group({'name':'Light 7','base_id':'7'}, 'Group 2')


        light_list = [ {'name':'Light 2','base_id':'2'},
                       {'name':'Light 3','base_id':'3'},
                       {'name':'Light 4','base_id':'4'},
                       {'name':'Light 5','base_id':'5'},
                       {'name':'Light 6','base_id':'6'},
                       {'name':'Light 7','base_id':'7'} ]

        add_lights_to_group(light_list, "Group 2")
        self.assertEquals(len(get_lights_in_group("Group 2")), len(light_list))

        group_three = Group(name='Group 3')

        # Add group 2 to group 3, query lights, query groups
        add_group_to_group("Group 2", "Group 3")
        self.assertEquals(len(get_lights_in_group("Group 3")), len(light_list))

        group_three_size = len(light_list) + 1
        add_group_to_group("Group 1", "Group 3")
        self.assertEquals(len(get_lights_in_group("Group 3")), group_three_size)

        # Make sure there are three created groups +1 for uncategorized
        self.assertEquals(len(get_groups()), 4)

        # Make sure the lights added to the database match up
        self.assertEquals(len(get_lights()), len(light_list)+1)

        group_three = Group(name='Group 4')

        # Add a ton of new lights and verify
        for i in range(0,MAX_LIGHTS):
            add_light_to_group({'name':'Bedroom %s'%i, "base_id":"%i"}, "Group 4")

        group_three_size += MAX_LIGHTS
        add_group_to_group("Group 4", "Group 3")
        self.assertEquals(len(get_lights_in_group('Group 4')), MAX_LIGHTS)
        self.assertEquals(len(get_lights_in_group('Group 3')), group_three_size)

################################################################################
# Setup Testcases to run
################################################################################

if __name__ == "__main__":
    unittest.main()