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
start_images = [load_and_scale(f'ASSET/START/start ({num}).png')for num in range(1, 13)]
loading_images = [load_and_scale(f'ASSET/LOADING/loading ({num}).png')for num in range(1, 23)]

#Load sounds
click_sound = pygame.mixer.Sound('SOUNDS/click.mp3')
pygame.mixer.music.load('SOUNDS/background music.mp3')
pygame.mixer.music.play(-1) #loop background music

#Loop to test asset loading

def asset_test():
    running = True
    clock = pygame.time.Clock()
    start_frame = 0
    loading_frame = 0
    start_loops = 0
    max_start_loops = 4 #times to loop start_images

    showing_start = True
    showing_loading = False

    while running:
        #screen.blit(quiz_template, (0, 0)) #show background image

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill((0, 0, 0))

        if showing_start:
            screen.blit(start_images[start_frame], (0, 0))
            pygame.time.delay(80) #to delay start images a lil bit
            start_frame += 1
            if start_frame >= len(start_images):
                start_frame = 0
                start_loops += 1
                if start_loops >= max_start_loops:
                    showing_start = False
                    showing_loading = True
        elif showing_loading:
            if loading_frame < len(loading_images):
                screen.blit(loading_images[loading_frame], (0, 0))
                pygame.time.delay(120) #to delay loading images since it's too fast
                loading_frame += 1
            else:
                running = False #close after animation

        pygame.display.flip()
        clock.tick(20)

    pygame.quit()
    sys.exit()

asset_test()