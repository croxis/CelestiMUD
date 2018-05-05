class ShipyardConsole(object):
    def at_object_creation(self):
        "This is called only when object is first created"
        #self.cmdset.add_default(default_cmds.CharacterCmdSet)
        #self.cmdset.add(ShipyardCmdSet, permanent=True)
        #self.locks.add("puppet:all();call:false()")
        self.db.desc = "Interface to manufacture your ship."