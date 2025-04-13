#Import necessary modules
import sys
import pygame
import pygame.locals import
from pyrect import WIDTH *

#initialize pygame and mixer(for sound)
pygame.init()
pygame.mixer.init()

#Setup Display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Creator")

#Font
font = pygame.font.Sysfont("Courier, 40")
small_font = pygame.font.Sysfont("Courier, 30")

#For easier load and scale images
def load_and_scale(path):
    return pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))

