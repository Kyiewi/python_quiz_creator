#Import necessary modules
import sys
import pygame
from pygame.constants import USEREVENT
from pygame.locals import *

#initialize pygame and mixer(for sound)
pygame.init()
pygame.mixer.init()

#Setup Display
WIDTH, HEIGHT = 850, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Creator")

#Font
font = pygame.font.SysFont("Courier", 30)
small_font = pygame.font.SysFont("Courier", 20)

#Color
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)

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

#---------------INPUTBOX CLASS--------------

class InputBox:
    def __init__(self, x, y, w, h, text='', dynamic_width=True):
        #rectangle area for input box
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.txt_surface = font.render(text, True, WHITE)
        self.active = False
        self.dynamic_width = dynamic_width

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            #activate box if clicked inside, otherwise deactivate
            self.active = self.rect.collidepoint(event.pos)
            #border
            self.color = (225, 0, 0) if self.active else WHITE

        #check for key presses when box is active
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                #deactivate box on enter
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                #remove last character
                self.text = self.text[:-1]
            else:
                #add typed character
                self.text += event.unicode
            self.txt_surface = font.render(self.text, True, WHITE) #re-render the updated text in white

    def update(self):
        #remove or adjust forced minimum width
        if self.dynamic_width:
            self.rect.w = self.txt_surface.get_width() + 200

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=2, border_radius=5) #border of input
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y +5)) #text surface

    def clear(self):
        self.text = '' #clear input box text
        self.txt_surface = font.render(self.text, True, WHITE)

#input boxes fields for quiz data
boxes = [
    InputBox(72, 61, 40, 40, dynamic_width=False), # Question number
    InputBox(136, 66, 200, 40), # Question text
    InputBox(214, 165, 200, 40), # Choice A
    InputBox(220, 267, 200, 40), # Choice B
    InputBox(495, 164, 200, 40), # Choice C
    InputBox(499, 267, 200, 40), # Choice D
    InputBox(427, 368, 80, 40, dynamic_width=False), # Correct answer

]

# -----------------BUTTONS--------------------
start_button = pygame.Rect(319, 320, 200, 50)
enter_button = pygame.Rect(201, 470, 150, 50)
quit_button = pygame.Rect(500, 470, 150, 50)
yes_button = pygame.Rect(152, 371, 190, 65)
no_button = pygame.Rect(494, 371, 190, 65)

#Flags
saved_message = ''
save_counter = 0
showing_start = True
showing_loading = False
showing_quiz = False
showing_exit_confirm = False
showing_sad = False

#Main functions

def main():
    running = True
    clock = pygame.time.Clock()
    start_frame = 0
    loading_frame = 0

    global showing_start, showing_loading, showing_quiz, showing_exit_confirm, showing_sad, saved_message, save_counter

    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            #to detect click button
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse clicked at:", event.pos) # to get coordinates
                if showing_start and start_button.collidepoint(event.pos):
                    click_sound.play() #play sound upon detection
                    showing_start = False
                    showing_loading = True
                    loading_frame = 0 #reset loading animation

                elif showing_quiz:
                    if enter_button.collidepoint(event.pos):
                        click_sound.play()
                        #to record user input and output it as a txt file
                        with open('quiz_data.txt', 'a') as f:
                            f.write(f"Number:{boxes[0].text}\n")
                            f.write(f"Question:{boxes[0].text}\n")
                            f.write(f"A:{boxes[0].text}\n")
                            f.write(f"B:{boxes[0].text}\n")
                            f.write(f"C:{boxes[0].text}\n")
                            f.write(f"D:{boxes[0].text}\n")
                            f.write(f"Correct Answer:{boxes[0].text}\n")
                        saved_message = 'Saved!' #save notif for user
                        save_counter = pygame.time.get_ticks()
                        for box in boxes:
                            box.clear()

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

            if showing_quiz:
                for box in boxes:
                    box.handle_event(event)

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

            for box in boxes:
                box.update()
                box.draw(screen)

            if saved_message and pygame.time.get_ticks() - save_counter < 2000:
                saved_text = small_font.render(saved_message, True, WHITE)
                screen.blit(saved_text, (WIDTH // 2 - saved_text.get_width() // 2, HEIGHT - 50))
            else:
                saved_message = ''

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

if __name__ == "__main__":
    main()