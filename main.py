import pygame,sys

from map import * 
from entity import *
from settings import *

from inventory import *
from FOV import FOV
from GUI import GUI

class Game:
    def __init__(self, width=screen_width, height=screen_height, title="Roguelike"):
        pygame.init()

        self.width = width
        self.height = height
        self.title = title

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        self.game_state = "playing"

        # Initialize map
        self.map = Map(self.width // tile_size, self.height // tile_size)

        root_room = Room(0, 0, self.width // tile_size, self.height // tile_size)
        root_node = BSPNode(root_room)
        root_node.build_tree()
        root_node.create_dungeon(self.map)

        # Create player character
        self.player = Player(160, 160, (255, 255, 0),self.map,"Player",100,20)
        self.monster = BasicMonster(128,160,COLOR_RED,self.map,"Evil",100)
        self.Fov = FOV()
        self.GUI = GUI()

        # List to hold all entities

        self.entities = [self.player,self.monster]

        
        
    def handle_events(self):
        # Check if entity is dead
        for entity in self.entities:
            if entity.status == "Dead":
                self.clear(entity)
        for event in pygame.event.get():
            if self.player.status == "Dead":
                self.game_state = "quit"
            else:
                if event.type == pygame.QUIT:
                    self.game_state = "quit"

                if self.game_state == "playing":
                    if self.player.handle_events(event, self.map,self.entities):
                        if self.player.player_action == "took-turn":
                            for entity in self.entities:
                                if entity != self.player:
                                    entity.take_turn(self.player,self.map)
                                    self.player.player_action = None

                        # değişebilir
                        self.Fov.compute_fov(self.map,self.player.x//tile_size,self.player.y//tile_size,8,self.screen)

                            
                   
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_map()
        self.GUI.draw_health_bar(self.screen,self.player)

        for entity in self.entities:
            entity.draw(self.screen)

        pygame.display.flip()

    def draw_map(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                tile = self.map.map[y][x]
                ## Tile is visible now
                if tile.visible:
                    if tile.blocked:
                        pygame.draw.rect(self.screen, COLOR_GREY, rect)
                    else:
                        pygame.draw.rect(self.screen, COLOR_WHITE, rect)


                elif tile.explored:
                    # tile explored and blocked
                    if tile.blocked:
                        pygame.draw.rect(self.screen, (30, 30, 30), rect)
                    else:
                        # tile explored and not blocked
                        pygame.draw.rect(self.screen, (80, 80, 80), rect)

                else:
                    pygame.draw.rect(self.screen, COLOR_BLACK, rect)


                

    def clear(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def run(self):
        while self.game_state == "playing":
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()