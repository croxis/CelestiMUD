# Much code from the evennia mapbuilder example

from evennia import Command, create_object
from evennia import CmdSet
from evennia import default_cmds

from typeclasses import rooms


def build_bridge(x, y, **kwargs):
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


class CmdCreate(Command):
    """
    Create a new vanilla ship.

    Usage:
      create ship [class]

    This will create a new ship. If no
    class is given, a new basic 4 person ship will be created.
    """
    key = "build ship"
    aliases = ["spawn ship"]

    def func(self):
        """This actually does the shooting"""

        caller = self.caller
        location = caller.location

        if not self.args:
            # no argument given to command - shoot in the air
            message = "Creating a cute little ship that an pew pew pew!"
            location.msg_contents(message)
            return

        # we have an argument, search for target
        target = caller.search(self.args)
        if target:
            message = "Creating a fancy %s" % target.key
            location.msg_contents(message)


class ShipyardCmdSet(CmdSet):
    """
    Constructing ships to pilot around
    """
    key = "shipyardcmdset"

    def at_cmdset_creation(self):
        """Called once, when cmdset is first created"""
        self.add(CmdCreate())
