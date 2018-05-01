# Much code from the evennia mapbuilder example

from django.conf import settings
from evennia import Command, create_object
from evennia import CmdSet
from evennia import default_cmds
from evennia.utils import utils

from typeclasses import exits, rooms


# Helper function for readability.
def _map_to_list(game_map):
    """
    Splits multi line map string into list of rows, treats for UTF-8 encoding.

    Args:
        game_map (str): An ASCII map

    Returns:
        list (list): The map split into rows

    """
    list_map = game_map.split('\n')
    return [character.decode('UTF-8') if isinstance(character, basestring)
            else character for character in list_map]


def build_map(caller, game_map, legend, iterations=1, build_exits=True):
    """
    Receives the fetched map and legend vars provided by the player.

    Args:
        caller (Object): The creator of the map.
        game_map (str): An ASCII map string.
        legend (dict): Mapping of map symbols to object types.
        iterations (int): The number of iteration passes.
        build_exits (bool): Create exits between new rooms.

    Notes:
        The map
        is iterated over character by character, comparing it to the trigger
        characters in the legend var and executing the build instructions on
        finding a match. The map is iterated over according to the `iterations`
        value and exits are optionally generated between adjacent rooms according
        to the `build_exits` value.

    """

    # Split map string to list of rows and create reference list.
    caller.msg("Building ship...")
    caller.msg(game_map)
    game_map = _map_to_list(game_map)

    # Create a reference dictionary which be passed to build functions and
    # will store obj returned by build functions so objs can be referenced.
    room_dict = {}

    caller.msg("Attaching rooms to superstructure...")
    for iteration in xrange(iterations):
        for y in xrange(len(game_map)):
            for x in xrange(len(game_map[y])):
                for key in legend:
                    # obs - we must use == for unicode
                    if utils.to_unicode(game_map[y][x]) == utils.to_unicode(key):
                        room = legend[key](x, y, iteration=iteration,
                                           room_dict=room_dict,
                                           caller=caller)
                        if iteration == 0:
                            room_dict[(x, y)] = room

    if build_exits:
        # Creating exits. Assumes single room object in dict entry
        caller.msg("Installing pressure doors...")
        for loc_key, location in room_dict.iteritems():
            x = loc_key[0]
            y = loc_key[1]

            # north
            if (x, y - 1) in room_dict:
                if room_dict[(x, y - 1)]:
                    create_object(exits.Exit, key="bow",
                                  aliases=["b", "n"], location=location,
                                  destination=room_dict[(x, y - 1)])

            # east
            if (x + 1, y) in room_dict:
                if room_dict[(x + 1, y)]:
                    create_object(exits.Exit, key="starbord",
                                  aliases=["e", "st"], location=location,
                                  destination=room_dict[(x + 1, y)])

            # south
            if (x, y + 1) in room_dict:
                if room_dict[(x, y + 1)]:
                    create_object(exits.Exit, key="stern",
                                  aliases=["s"], location=location,
                                  destination=room_dict[(x, y + 1)])

            # west
            if (x - 1, y) in room_dict:
                if room_dict[(x - 1, y)]:
                    create_object(exits.Exit, key="port",
                                  aliases=["w", "p"], location=location,
                                  destination=room_dict[(x - 1, y)])

    caller.msg("Ship Constructed.")


#TODO: Find out what this does
COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)


class CmdShipBuilder(COMMAND_DEFAULT_CLASS):
    """
    Build a ship from a 2D ASCII map.

    Usage:
        @shipbuilder <class>

    Example:
        @mapbuilder ROUNDABOUT

    This is a command which takes two inputs:
    A string of ASCII characters representing a map and a dictionary of
    functions containing build instructions. The characters of the map are
    iterated over and compared to a list of trigger characters. When a match
    is found the corresponding function is executed generating the rooms,
    exits and objects as defined by the users build instructions. If a
    character is not a match to a provided trigger character (including spaces)
    it is simply skipped and the process continues. By default exits are
    automatically generated but is turned off by switches which also determines
    how many times the map is iterated over.
    """
    key = "@shipbuilder"
    aliases = ["@buildship"]
    help_category = "Building"

    def func(self):
        """Starts the processor."""

        caller = self.caller
        args = self.args.split()

        # Check if arguments passed.
        if not self.args or (len(args) != 1):
            caller.msg("Usage: @shipbuilder <CLASS>")
            return

        # Set up base variables.
        game_map = None
        legend = None

        # OBTAIN MAP FROM MODULE

        # Breaks down path_to_map into [PATH, VARIABLE]
        ship_class = args[0]
        path_to_ship_class = ship_class.rsplit('.', 1)


        try:
            # Retrieves map variable from module or raises error.
            game_map = utils.variable_from_module(path_to_ship_class[0],
                                                  path_to_ship_class[1])
            if not game_map:
                raise ValueError("Command Aborted!\n"
                                 "Path to map variable failed.\n"
                                 "Usage: @shipbuilder <world.ships.TYPE.SHIPCLASS>")

        except Exception as exc:
            # Or relays error message if fails.
            caller.msg(exc)
            return

        # OBTAIN MAP_LEGEND FROM MODULE

        # Breaks down path_to_legend into [PATH, VARIABLE]
        legend = args[0]
        # Strong arming the legend from the module. Need a better method me thinks
        path_to_legend = ['.'.join(legend.split('.')[:3]), 'LEGEND']

        try:
            # Retrieves legend variable from module or raises error if fails.
            legend = utils.variable_from_module(path_to_legend[0],
                                                path_to_legend[1])
            if not legend:
                raise ValueError("Command Aborted!\n"
                                 "Path to map variable failed.\n"
                                 "Usage: @shipbuilder <world.ships.TYPE.SHIPCLASS>")

        except Exception as exc:
            # Or relays error message if fails.
            caller.msg(exc)
            return

        # Set up build_map arguments from switches
        iterations = 1
        build_exits = True

        # Pass map and legend to the build function.
        build_map(caller, game_map, legend, iterations, build_exits)


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
