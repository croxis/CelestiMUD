from evennia import create_object
from typeclasses import exits, rooms

from .ships import *


def build_bridge(x, y, **kwargs):
    # If on anything other than the first iteration - Do nothing.
    if kwargs["iteration"] > 0:
        return None

    room = create_object(rooms.Room, key="bridge" + str(x) + str(y))
    room.db.desc = "Bridge of the ship."

    # Send a message to the account
    kwargs["caller"].msg(room.key + " " + room.dbref)

    captains_chair = create_object(key="Chair", location=room)
    captains_chair.db.desc = "The captain's chair."

    stations = ["navigation", "weapons", "engineering", "communications", "science"]
    for station in stations:
        chair = create_object(key="Chair", location=room)
        chair.db.desc = "Chair for " + station
        console = create_object(key="Console: " + station)
        console.db.desc = "Console for " + station

    # Mandatory, usually
    return room


def build_common(x, y, **kwargs):
    # If on anything other than the first iteration - Do nothing.
    if kwargs["iteration"] > 0:
        return None

    room = create_object(rooms.Room, key="common" + str(x) + str(y))
    room.db.desc = "Common room found on smaller ship. A combination of galley, dining, and rec room."

    # Send a message to the account
    kwargs["caller"].msg(room.key + " " + room.dbref)

    table = create_object(key="Table", location=room)
    table.db.desc = "A simple table with outstanding, outdated, Swedish mass produced minimalistic design."
    for i in range(0, 2):
        chair = create_object(key="Chair", location=room)
        chair.db.desc = "A simple dented metallic chair. Worn sleeping pillows provide ample padding for ample seats."

    # Mandatory, usually
    return room

def build_vertical_exit(x, y, **kwargs):
    """Creates two exits to and from the two rooms north and south."""
    if kwargs["iteration"] == 0:
        return

    north_room = kwargs["room_dict"][(x, y - 1)]
    south_room = kwargs["room_dict"][(x, y + 1)]

    # create exits in the rooms
    create_object(exits.Exit, key="south",
                  aliases=["s"], location=north_room,
                  destination=south_room)

    create_object(exits.Exit, key="north",
                  aliases=["n"], location=south_room,
                  destination=north_room)

    kwargs["caller"].msg("Connected: " + north_room.key +
                         " & " + south_room.key)


def build_horizontal_exit(x, y, **kwargs):
    """Creates two exits to and from the two rooms east and west."""
    # If on the first iteration - Do nothing.
    if kwargs["iteration"] == 0:
        return

    west_room = kwargs["room_dict"][(x - 1, y)]
    east_room = kwargs["room_dict"][(x + 1, y)]

    create_object(exits.Exit, key="east",
                  aliases=["e"], location=west_room,
                  destination=east_room)

    create_object(exits.Exit, key="west",
                  aliases=["w"], location=east_room,
                  destination=west_room)

    kwargs["caller"].msg("Connected: " + west_room.key +
                         " & " + east_room.key)


LEGEND = {("|"): build_vertical_exit,
          ("-"): build_horizontal_exit,
          ("B"): build_bridge,
          ("C"): build_common}
