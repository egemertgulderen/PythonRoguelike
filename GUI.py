from settings import *
import pygame
class GUI:
    def __init__(self) ->None:
        self.font = pygame.font.SysFont(None, 24)
        self.message_log = []
        self.max_messages = 5

    def draw_health_bar(self,screen,player):
        max_health = player.max_health
        health = player.health
        health_ratio = health / max_health
        filled_width = int(health_ratio * 200)

        pygame.draw.rect(screen, (255, 0, 0), (main_game_width + 10, 10, 180, 30))  # Right panel health bar background
        pygame.draw.rect(screen, (0, 255, 0), (main_game_width + 10, 10, filled_width, 30))  # Health fill

        health_text = self.font.render(f"Health: {health}/{max_health}", True, (255, 255, 255))
        screen.blit(health_text, (main_game_width + 15, 15))

    
    def draw_message_block(self,screen):
        x, y = 10, main_game_height + 10  # Start from the bottom panel area
        for message in self.message_log:
            message_text = self.font.render(message, True, (255, 255, 255))
            screen.blit(message_text, (x, y))
            y += 20



    def add_message(self, message):
        self.message_log.append(message)
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)