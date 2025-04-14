#Import necessary modules
import sys
import pygame
from pygame.constants import USEREVENT
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

#Main functions

def main():
    running = True
    clock = pygame.time.Clock()
    start_frame = 0
    loading_frame = 0

    showing_start = True
    showing_loading = False
    showing_quiz = False
    showing_exit_confirm = False
    showing_sad = False

    #-----------------BUTTONS--------------------
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2+100, 200, 50)
    enter_button = pygame.Rect(WIDTH // 4 - 75, HEIGHT - 100, 150, 50)
    quit_button = pygame.Rect(WIDTH * 3 // 4 - 75, HEIGHT - 100, 150, 50)
    yes_button = pygame.Rect(WIDTH // 4 - 75, HEIGHT - 100, 150, 50)
    no_button = pygame.Rect(WIDTH * 3 // 4 - 75, HEIGHT - 100, 150, 50)

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

                elif showing_quiz:
                    if enter_button.collidepoint(event.pos):
                        click_sound.play()
                        print("Enter quiz creation...") #placeholder for now
                    elif quit_button.collidepoint(event.pos):
                        click_sound.play()
                        showing_quiz = False
                        showing_exit_confirm = True

                elif showing_exit_confirm:
                    if yes_button.collidepoint(event.pos):
                        click_sound.play()
                        showing_exit_confirm = False
                        showing_sad = True
                        pygame.time.set_timer(USEREVENT + 1, 2000) #show sad image for 2 secs
                    elif no_button.collidepoint(event.pos):
                        click_sound.play()
                        showing_exit_confirm = False
                        showing_quiz = True

            if event.type == USEREVENT +1:
                pygame.quit()
                sys.exit()

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
            # ENTER  BUTTON
            pygame.draw.rect(screen, (255, 255, 255), enter_button, border_radius=12)
            screen.blit(font.render("ENTER", True, (0, 0, 0)), (enter_button.x + 45, enter_button.y +10))

            # QUIT BUTTON
            pygame.draw.rect(screen, (255, 255, 255), quit_button, border_radius=12)
            screen.blit(font.render("QUIT", True, (0, 0, 0)), (quit_button.x + 45, quit_button.y + 10))

        elif showing_exit_confirm:
            screen.blit(exit_image, (0, 0))  # show background image
            # YES BUTTON
            pygame.draw.rect(screen, (255, 255, 255), yes_button, border_radius=12)
            screen.blit(font.render("YES", True, (0, 0, 0)), (yes_button.x + 45, yes_button.y + 10))

            # NO BUTTON
            pygame.draw.rect(screen, (255, 255, 255), no_button, border_radius=12)
            screen.blit(font.render("NO", True, (0, 0, 0)), (no_button.x + 45, no_button.y + 10))

        elif showing_sad:
            screen.blit(sad_image, (0, 0))  # show background image

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()
    sys.exit()

main()