import pygame

from FOV import FOV
from settings import *



class Entity:
    def __init__(self, x, y, color,blocked= False,name=None,health = 100):
        self.x = x
        self.y = y
        self.color = color
        self.size = tile_size
        self.blocked = blocked
        self.name = name
        self.health = health

    def handle_events(self, event, game_map):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))

    def move(self, dx, dy, game_map):
        moved = False
        new_x = self.x + dx
        new_y = self.y + dy

        if not game_map.is_blocked(new_x//tile_size,new_y//tile_size):
            self.x = new_x
            self.y = new_y
            moved = True

        return moved
    def move_or_attack(self,dx,dy,game_map,entities):
        moved = False
        new_x = self.x + dx
        new_y = self.y + dy

        if not game_map.is_blocked(new_x//tile_size,new_y//tile_size):
            self.x = new_x
            self.y = new_y
            moved = True

        else:
            for entity in entities:
                if entity.x == new_x and entity.y == new_y:
        
                    self.attack(entity)
                    print("Player attackted" + str(entity.name))

    def get_coordinates(self):
        return self.x, self.y
    
    def get_health(self):
        return self.health
    
    
    def attack(self,entity):
        pass

class Player(Entity):
    def __init__(self, x, y, color,blocked,name,health):
        super().__init__(x, y, color,blocked=False,name=None,health=100)
        self.direction = 0
        self.blocked = True
        self.health = health
        self.name = "Player" 

    def handle_events(self, event, game_map,entitites):
        moved = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.move_or_attack(-self.size, 0, game_map,entitites):
                    moved = True
            elif event.key == pygame.K_RIGHT:
                if self.move_or_attack(self.size, 0, game_map,entitites):
                    moved = True

            elif event.key == pygame.K_UP:
                if self.move_or_attack(0, -self.size, game_map,entitites):
                    moved = True

            elif event.key == pygame.K_DOWN:
                if self.move_or_attack(0, self.size, game_map,entitites):
                    moved = True

        return moved
    
    def move_or_attack(self,dx,dy,game_map,entities):
        moved = False
        new_x = self.x + dx
        new_y = self.y + dy

        if not game_map.is_blocked(new_x//tile_size,new_y//tile_size):
            self.x = new_x
            self.y = new_y
            moved = True

        else:
            for entity in entities:
                if entity.x == new_x and entity.y == new_y:
        
                    self.attack(entity)
                    print("Player attackted" + str(entity.name))

        return moved


    def get_health(self):
        return self.health
    
    
    def attack(self,entity):
        pass
