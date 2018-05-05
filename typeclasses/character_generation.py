from evennia import CmdSet, Command
from evennia.utils import evmenu


class CmdCharGen(Command):
    """
    Create a character
    """

    def func(self):
        """Start menu instance."""
        evmenu.EvMenu(self.caller,
                      "typeclassess.chargen",
                      startnode="menu_start")


class CharGenCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdCharGen())


def _if_newbie(caller, raw_string):
    if caller.db.newbie:
        return "menu_chargen"


def start(caller):
    text = "Wa koming gut!"
    options = ({"desc": "Create a charater",
                "goto": "menu_chargen",
                "exec": _if_newbie},
               {"desc": "Continue existing character",
                "goto": "start_game"})
    return text, options


def menu_chargen(caller):
    """Top menu screen for character generation."""
    text = "Welcome to Character Generation!"
    options = []
    options.append({"desc": "Set name", "goto": "menunode_set_name"})
    options.append({"desc": "Set age", "goto": "menunode_set_age"})
    options.append({"desc": "Set weight", "goto": "menunode_set_mass"})
    options.append({"desc": "Set birthplace", "goto": "menunode_set_birthplace"})
    return text, options


def _set_name(caller, raw_string):
    inp = raw_string.stript()
    if not inp:
        caller.msg("Aborted.")
    else:
        caller.key = inp
        caller.msg("Name set to %s." % caller.key)


def menu_set_name(caller, raw_string):
    """Sets up the set name screen"""
    text = "What is your character's name or <return> to abort?"
    options = ({"key": "_default",
                "exec": _set_name,
                "goto": "menu_chargen"})
    return text, options


def _set_age(caller, raw_string):
    inp = raw_string.stript()
    try:
        float(inp)
    except ValueError:
        caller.msg("Please enter a number. Aborted.")


def menu_set_age(caller, raw_input):
    """Sets up the set age screen"""
    text = "What's your character's age"
    options = ({"key": "_default",
                "exec": _set_age,
                "goto": "menu_chargen"})
    return text, options


def _set_mass(caller, raw_string):
    inp = raw_string.stript()
    try:
        float(inp)
    except ValueError:
        caller.msg("Please enter a number. Aborted.")


def menu_set_mass(caller, raw_input):
    """Sets up the set mass screen"""
    text = "How heavy is your character?"
    options = ({"key": "_default",
                "exec": _set_mass,
                "goto": "menu_chargen"})
    return text, options


def menu_set_birthplace(caller, raw_input):
    """Sets up the set age screen"""
    text = "Where were you born?"
    options = []
    options.append({"text": "Earth"})
    options.append({"text": "Mars"})
    options.append({"text": "Low G"})
    return text, options
