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

    showing_start = True
    showing_loading = False
    showing_quiz = False

    #draw start button (test)
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2+100, 200, 50)

    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            #to detect click button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if showing_start and start_button.collidepoint(event.pos):
                    click_sound.play() #play sound upon detection
                    showing_start = False
                    showing_loading = True
                    loading_frame = 0 #reset loading animation

        screen.fill((0, 0, 0))

        if showing_start:
            screen.blit(start_images[start_frame], (0, 0))
            pygame.draw.rect(screen,(255 , 255, 255), start_button, border_radius=12)
            screen.blit(font.render("START", True, (0, 0, 0)), (start_button.x + 45, start_button.y +10))
            pygame.time.delay(80) #to delay start images a lil bit

            start_frame = (start_frame +1) %len(start_images)

        elif showing_loading:
            if loading_frame < len(loading_images):
                screen.blit(loading_images[loading_frame], (0, 0))
                pygame.time.delay(120) #to delay loading images since it's too fast
                loading_frame += 1
            else:
                showing_loading = False #close after animation
                showing_quiz = True

        elif showing_quiz:
            screen.blit(quiz_template, (0, 0)) #show background image

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()
    sys.exit()

asset_test()