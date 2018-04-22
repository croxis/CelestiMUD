from evennia import Command
from evennia import CmdSet
from evennia import default_cmds


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
