#Import necessary modules
import sys
import pygame
from pygame.locals import *

#initialize pygame and mixer(for sound)
pygame.init()
pygame.mixer.init()

#Setup Display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Creator")

#Font
font = pygame.font.SysFont("Courier", 40)
small_font = pygame.font.SysFont("Courier", 30)

#For easier load and scale images
def load_and_scale(path):
    return pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))

#-------ASSETS--------

#Load Background images
quiz_template = load_and_scale('ASSET/quiz_template.png')
sad_image = load_and_scale('ASSET/sad.png')
exit_image = load_and_scale('ASSET/Exit.png')

#Load animations
start_images = [load_and_scale(f'ASSET/START/start ({num}).png)')for num in range(1, 13)]
loading_images = [load_and_scale(f'ASSET/LOADING/loading ({num}.png)')for num in range(1, 23)]

#Load sounds
click_sound = pygame.mixer.Sound('SOUNDS/click.mp3')
pygame.mixer.music.load('SOUNDS/background music.mp3')
pygame.mixer.music.play(-1) #loop background music


