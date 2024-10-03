import pygame
import math

from settings import *
from inventory import *
from FOV import *
class Entity:
    def __init__(self, x, y, color,game_map,name=None,health = 100,damage= 10):
        self.x = x
        self.y = y
        self.color = color
        self.size = tile_size
        self.name = name
        self.max_health = health
        self.health = health

        self.block_current_tile(game_map)
        self.damage = damage
        self.status = "Alive"

        self.fov = FOV()
        


    def block_current_tile(self, game_map):
        """Mark the current tile as blocked."""
        tile_x = self.x // tile_size
        tile_y = self.y // tile_size
        game_map.set_block(tile_x, tile_y)

    def unblock_current_tile(self, game_map):
        """Mark the current tile as unblocked."""
        tile_x = self.x // tile_size
        tile_y = self.y // tile_size
        game_map.set_unblock(tile_x, tile_y)

    def handle_events(self, event, game_map):
        pass

    def draw(self, screen, tiles, tile_index):
        if self.name == "Player":
            tile = tiles[25]
            screen.blit(tile, (self.x, self.y))
        else:
            tile = tiles[tile_index]
            screen.blit(tile, (self.x, self.y))

    def get_coordinates(self):
        return self.x, self.y
    

    def get_health(self):
        return self.health
    
    def move_toward(self,target_x,target_y,game_map):
        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        dx = int(round(dx /distance))
        dy = int(round(dy / distance))
        
        self.move(dx*tile_size,dy*tile_size,game_map)

    def distance_to(self,other):
        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx**2 + dy**2)
    
    def move(self, dx, dy, game_map):
        moved = False
        new_x = self.x + dx
        new_y = self.y + dy

        if not game_map.is_blocked(new_x//tile_size,new_y//tile_size):
            self.unblock_current_tile(game_map)
            self.x = new_x
            self.y = new_y
            self.block_current_tile(game_map)

            moved = True

        return moved
    

    def move_or_attack(self,dx,dy,game_map,entities, gui):
        moved = False
        attacked = False
        new_x = self.x + dx
        new_y = self.y + dy

        if not game_map.is_blocked(new_x//tile_size,new_y//tile_size):
            self.unblock_current_tile(game_map)
            self.x = new_x
            self.y = new_y
            self.block_current_tile(game_map)
            moved = True

        else:
            for entity in entities:
                if entity.x == new_x and entity.y == new_y:

                    self.attack(entity,game_map, gui)
                    attacked = True
    
        if attacked or moved:
            return True
        else:
            return False
        

    def take_damage(self,damage_amount,game_map):
        if damage_amount > 0:
            self.health -= damage_amount
        
        if self.health <= 0:
            self.status = "Dead"
            self.unblock_current_tile(game_map)
            
    def attack(self,entity,game_map, gui):
        entity.take_damage(self.damage,game_map)
        message = f"{self.name} attacked {entity.name}!"
        gui.add_message(message)  # Send message to GUI log


class Player(Entity):
    def __init__(self, x, y, color, game_map, name=None, health=100, damage=10):
        super().__init__(x, y, color, game_map, name, health, damage)
        self.direction = 0
        self.name = "Player" 
        self.player_action = None
        self.class_component = None
        self.damage = damage
        

        self.inventory = Inventory(10) # type: ignore


    def handle_events(self, event, game_map,entitites, gui):
        moved = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.move_or_attack(-self.size, 0, game_map,entitites, gui):
                    moved = True
            elif event.key == pygame.K_RIGHT:
                if self.move_or_attack(self.size, 0, game_map,entitites, gui):
                    moved = True

            elif event.key == pygame.K_UP:
                if self.move_or_attack(0, -self.size, game_map,entitites, gui):
                    moved = True

            elif event.key == pygame.K_DOWN:
                if self.move_or_attack(0, self.size, game_map,entitites, gui):
                    moved = True

        if moved:
            self.player_action = "took-turn"
        return moved
    
    def inventory(self):
        pass


class BasicMonster(Entity):
    def __init__(self, x, y, color, game_map, name=None, health=100, damage=10):
        super().__init__(x, y, color, game_map, name, health, damage)

    def take_turn(self,player,game_map, gui):
        # if can see player

        if self.distance_to(player) >= 2*tile_size:
            self.move_toward(player.x,player.y,game_map)

        else:
            self.attack(player,game_map, gui)

