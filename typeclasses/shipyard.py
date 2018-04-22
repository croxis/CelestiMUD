
from objects import Object
from commands.makeShipCommands import ShipyardCmdSet
from evennia import default_cmds

class Shipyard(Object):
    """
    This typeclass describes an armed Mech.
    """
    def at_object_creation(self):
        "This is called only when object is first created"
        self.cmdset.add_default(default_cmds.CharacterCmdSet)
        self.cmdset.add(ShipyardCmdSet, permanent=True)
        self.locks.add("puppet:all();call:false()")
        self.db.desc = "This is a huge mech. It has missiles and stuff."