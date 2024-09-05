from entity import *

from settings import *

def create_player(x, y, map):
    """Creates the player entity."""
    return Player(x, y, (255, 255, 0), map, "Player", health=100, damage=20)

def create_monster(x, y, map, monster_type="basic"):
    """Creates a monster entity based on type."""
    if monster_type == "basic":
        return BasicMonster(x, y, COLOR_RED, map, "Evil", health=50)
    # Add more monster types here later if needed