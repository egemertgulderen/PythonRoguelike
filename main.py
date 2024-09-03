import pygame,sys

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)
from map import * 
from entity import *
from settings import *

from FOV import FOV

class Game:
    def __init__(self, width=screen_width, height=screen_height, title="Roguelike"):
        pygame.init()

        self.width = width
        self.height = height
        self.title = title

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        self.running = True



        # Initialize map
        self.map = Map(self.width // tile_size, self.height // tile_size)

        root_room = Room(0, 0, self.width // tile_size, self.height // tile_size)
        root_node = BSPNode(root_room)
        root_node.build_tree()
        root_node.create_dungeon(self.map)

        # Create player character
        self.player = Player(160, 160, (255, 255, 0),True,"Player",100)

        self.Fov = FOV()
        # List to hold all entities
        self.entities = [self.player]

        self.game_state = 'playing'
        
        
    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.player.handle_events(event, self.map,self.entities):
                    self.Fov.compute_fov(self.map,self.player.x//tile_size,self.player.y//tile_size,8,self.screen)
            
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_map()
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
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()