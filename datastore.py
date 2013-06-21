""" Data store for dr_hue """

from elixir import *
import os

DATABASE_LOCATION = "$HOME/.config/dr_hue.db"
UNCATEGORIZED     = "uncatagorized"

metadata.bind = "sqlite:///%s" % os.path.expandvars(DATABASE_LOCATION)
#metadata.bind.echo = True

class Group(Entity):
    """ Group Object """
    name = Field(String)
    has_many('lights', of_kind='Light')
    has_many('groups', of_kind='Group')
    belongs_to('group', of_kind='Group')

class Light(Entity):
    """ Light object """
    name = Field(String)
    base_id = Field(Integer)
    belongs_to('group', of_kind='Group')

def setup_database():
    """ Initialize the database with the tables """
    setup_all()
    create_all()

    if Group.get_by(name=UNCATEGORIZED) is None:
        Group(name=UNCATEGORIZED)

    session.commit()

def add_all_lights(lights):
    """ Add all lights to the database, defaulting to uncategorized """
    # Add all lights to uncatagorized cluster
    for light in lights:
        new_light = Light()
        new_light.name = light['name']
        new_light.base_station_id = light['base_id']
    session.commit()

def add_light_to_group(light_obj, group_name):
    """ Add a light to a group """
    group = Group.get_by(name=group_name)
    if group is not None:
        light_name = light_obj['name']
        light_id   = light_obj['base_id']
        light = Light.get_by(name=light_name)
        if light is not None:
            light.group_id = group.id
        else:
            new_light = Light()
            new_light.name = light_name
            new_light.base_station_id = light_id
            new_light.group_id = group.id
    else:
        raise Exception("Group name not found")

    session.commit()

def add_lights_to_group(lights, group_name):
    """ Add all lights to a group """
    _ = [add_light_to_group(light, group_name) for light in lights]

def add_group_to_group(group_to_add, group_to_contain):
    """ Add a group to a group """
    # Find the cluster by name
    container = Group.get_by(name=group_to_contain)
    to_store = Group.get_by(name=group_to_add)
    if container is not None and to_store is not None:
        to_store.group_id = container.id
    else:
        raise Exception("Group name not found")

    session.commit()

def get_light_in_group(light_name, group_name):
    """ Get a light in a given group """

    group = Group.query.filter_by(name=group_name).one()
    light = Light.query.filter_by(name=light_name).one()

    if group.id == light.group_id:
        return {light.name:light.base_id}
    else:
        return {}

def get_lights_in_group(group_name):
    """ Get all lights within a group """

    group    = Group.query.filter_by(name=group_name).one()
    group_id = group.id
    lights   = {light.name:light.base_id for light in Light.query.filter_by(group_id=group_id)}

    # For all the groups inside the given group, grab the lights
    for i in Group.query.filter_by(group_id=group_id):
        lights.update(get_lights_in_group(i.name))

    return lights

def get_lights():
    """ Get all lights in the database """
    return {light.name:light.base_id for light in Light.query.all()}

def get_groups():
    """ Get all groups in the database """
    return [group.name for group in Group.query.all()]

def purge():
    """ Reset to zero """
    _ = [light.delete() for light in Light.query.all()]
    _ = [group.delete() for group in Group.query.all()]
    session.commit()