from settings import *
import pygame
class GUI:
    def __init__(self) ->None:
        pass

    def draw_health_bar(self,screen,player):
        max_health = player.max_health
        health = player.health
        health_ratio = health / max_health
        filled_width = int(health_ratio * 50)

        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 50, 30))  # Red background
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, filled_width, 30))  # Green for current health

