import sys
import pygame
import random
from pygame.constants import USEREVENT
from pygame.locals import *

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Display settings
WIDTH, HEIGHT = 1060, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Game")

# Fonts & colors
font = pygame.font.SysFont("Courier", 25)
small_font = pygame.font.SysFont("Courier", 20)
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)

# Helper to load and fit images
def load_and_scale(path):
    return pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))

# Assets
quiz_template   = load_and_scale('ASSET 2/quiz_template.png')
sad_image       = load_and_scale('ASSET/sad.png')
exit_image      = load_and_scale('ASSET/Exit.png')
correct_image   = load_and_scale('ASSET/correct.png')
wrong_image     = load_and_scale('ASSET/wrong.png')
start_images    = [load_and_scale(f'ASSET 2/START/Start ({num}).png') for num in range(1, 13)]
loading_images  = [load_and_scale(f'ASSET/LOADING/loading ({num}).png') for num in range(1, 23)]

click_sound = pygame.mixer.Sound('SOUNDS/click.mp3')
pygame.mixer.music.load('SOUNDS/background music.mp3')
pygame.mixer.music.play(-1)

# Event for auto-advance after result
RESULT_TIMER = USEREVENT + 2

# InputBox class for creation and answer input
class InputBox:
    def __init__(self, x, y, w, h, text='', dynamic_width=True, editable=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.txt_surface = font.render(text, True, WHITE)
        self.active = False
        self.dynamic_width = dynamic_width
        self.editable = editable

    def handle_event(self, event):
        if not self.editable:
            return
        if event.type == MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = (225,0,0) if self.active else WHITE
        if event.type == KEYDOWN and self.active:
            if event.key == K_RETURN:
                self.active = False
            elif event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = font.render(self.text, True, WHITE)

    def update(self):
        if self.dynamic_width:
            self.rect.w = self.txt_surface.get_width() + 10

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

    def clear(self):
        self.text = ''
        self.txt_surface = font.render('', True, WHITE)

    def set_text(self, text):
        self.text = text
        self.txt_surface = font.render(text, True, WHITE)

# Boxes for quiz creation and placeholders for loaded question
boxes = [
    InputBox(43,  34, 40, 40, dynamic_width=False),  # Number
    InputBox(117, 38,200,40),                        # Question
    InputBox(171,158,200,40),                        # A
    InputBox(178,286,200,40),                        # B
    InputBox(615,164,200,40),                        # C
    InputBox(625,287,200,40),                        # D
    InputBox(645,392, 80,40, dynamic_width=False),   # Correct Answer
]
answer_input = InputBox(645,392,80,40, dynamic_width=False, editable=True)

# Buttons
create_button         = pygame.Rect(407, 320, 200, 50)
play_button          = pygame.Rect(454, 390, 200, 50)
enter_button         = pygame.Rect(201, 470, 150, 50)
quit_button          = pygame.Rect(807, 470, 150, 50)
submit_button        = pygame.Rect(120, 483, 150, 50)
back_button          = pygame.Rect(469, 476, 150, 50)
yes_button           = pygame.Rect(152, 371, 190, 65)
no_button            = pygame.Rect(728, 371, 190, 65)

# State flags
showing_start        = True
showing_create       = False
showing_exit_confirm = False
showing_sad          = False
showing_answer       = False
showing_result       = False
showing_loading = False
loading_target = None  # either "create" or "play"


saved_msg         = ''
save_time         = 0
is_correct        = False
current_question         = []
timer_set         = False

# Load a random question from file
def load_random_question():
    try:
        with open("quiz_data.txt") as f:
            parts = f.read().strip().split("Number:")
            question = [p for p in parts if p.strip()]
            return random.choice(question).splitlines()
    except:
        return []

# Draw Back/Quit buttons on template
def draw_back_and_quit():
    pygame.draw.rect(screen, WHITE, back_button, 2)
    screen.blit(small_font.render("Back", True, WHITE),(back_button.x+40, back_button.y+10))
    pygame.draw.rect(screen, WHITE, quit_button, 2)
    screen.blit(small_font.render("Quit", True, WHITE),(quit_button.x+40, quit_button.y+10))

# Main Loop
def main():
    global showing_start, showing_loading, loading_target, showing_create, showing_exit_confirm
    global showing_sad, showing_answer, showing_result, timer_set
    global saved_msg, save_time, is_correct, current_question

    clock = pygame.time.Clock()
    load_frame = start_frame = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Auto‑advance after result
            if event.type == RESULT_TIMER and showing_result:
                pygame.time.set_timer(RESULT_TIMER, 0)
                # load next Q and display
                current_question = load_random_question()
                for i, line in enumerate(current_question[:6]):
                    if ':' in line:
                        _, val = line.split(':',1)
                        boxes[i].set_text(val.strip())
                answer_input.clear()
                showing_result = False
                showing_answer = True

            if event.type == MOUSEBUTTONDOWN:
                print("Mouse clicked at:", event.pos)
                # Start menu
                if showing_start:
                    if create_button.collidepoint(event.pos):
                        click_sound.play()
                        showing_start = False
                        showing_loading = True
                        loading_target = "create"
                        load_frame = 0

                    elif play_button.collidepoint(event.pos):
                        click_sound.play()
                        showing_start = False
                        showing_loading = True
                        loading_target = "play"
                        load_frame = 0

                # Create quiz
                elif showing_create:
                    if enter_button.collidepoint(event.pos):
                        click_sound.play()
                        with open("quiz_data.txt","a") as f:
                            for idx, label in enumerate(["Number", "Question", "A", "B", "C", "D", "Correct Answer"]):
                                f.write(f"{label}:{boxes[idx].text}\n")
                        saved_msg="Saved!"; save_time=pygame.time.get_ticks(); [b.clear() for b in boxes]
                    elif back_button.collidepoint(event.pos):
                        click_sound.play(); [b.clear() for b in boxes]; showing_create=False; showing_start=True
                    elif quit_button.collidepoint(event.pos):
                        click_sound.play(); showing_create=False; showing_exit_confirm=True

                # Answer quiz
                elif showing_answer:
                    if submit_button.collidepoint(event.pos):
                        click_sound.play()
                        correct=next((ln.split(':',1)[1].strip() for ln in current_question if ln.startswith("Correct Answer:")),"")
                        is_correct=(answer_input.text.strip().lower()==correct.lower())
                        showing_answer=False; showing_result=True
                    elif back_button.collidepoint(event.pos):
                        click_sound.play(); showing_answer=False; showing_start=True
                    elif quit_button.collidepoint(event.pos):
                        click_sound.play(); showing_answer=False; showing_exit_confirm=True

                # Exit confirm
                elif showing_exit_confirm:
                    if yes_button.collidepoint(event.pos):
                        click_sound.play(); showing_exit_confirm=False; showing_sad=True; pygame.time.set_timer(USEREVENT+1,2000)
                    elif no_button.collidepoint(event.pos):
                        click_sound.play(); showing_exit_confirm=False; showing_create=True

            if event.type == USEREVENT+1:
                pygame.quit(); sys.exit()

            # pass events to boxes
            if showing_create: [b.handle_event(event) for b in boxes]
            if showing_answer: answer_input.handle_event(event)

        # Draw
        screen.fill(BLACK)
        if showing_start:
            screen.blit(start_images[start_frame],(0,0))
            pygame.draw.rect(screen,WHITE,create_button,2); screen.blit(small_font.render("Create Quiz",True,WHITE),(create_button.x+40,create_button.y+10))
            pygame.draw.rect(screen,WHITE,play_button,2); screen.blit(small_font.render("Answer Quiz",True,WHITE),(play_button.x+40,play_button.y+10))
            pygame.time.delay(80); start_frame=(start_frame+1)%len(start_images)


        elif showing_loading:
            if load_frame < len(loading_images):
                screen.blit(loading_images[load_frame], (0, 0))
                pygame.time.delay(120)
                load_frame += 1
            else:
                showing_loading = False
                if loading_target == "create":
                    showing_create = True
                    [b.clear() for b in boxes]
                elif loading_target == "play":
                    current_question = load_random_question()
                    for i, line in enumerate(current_question[:6]):
                        if ':' in line:
                            _, val = line.split(':', 1)
                            boxes[i].set_text(val.strip())

                    answer_input.clear()

                    showing_answer = True

                loading_target = None


        elif showing_create:
            screen.blit(quiz_template,(0,0))
            for b in boxes: b.update(); b.draw(screen)
            if saved_msg and pygame.time.get_ticks()-save_time<2000: screen.blit(small_font.render(saved_msg,True,WHITE),(WIDTH//2-50,HEIGHT-50))
            draw_back_and_quit()


        elif showing_answer:
            screen.blit(quiz_template,(0,0))
            # plain text for question/options
            for i in range(6): screen.blit(boxes[i].txt_surface,(boxes[i].rect.x+5,boxes[i].rect.y+5))
            answer_input.update(); answer_input.draw(screen)
            pygame.draw.rect(screen,WHITE,submit_button,2); screen.blit(small_font.render("Submit",True,WHITE),(submit_button.x+40,submit_button.y+10))
            pygame.draw.rect(screen,WHITE,back_button,2); screen.blit(small_font.render("Back",True,WHITE),(back_button.x+40,back_button.y+10))
            pygame.draw.rect(screen,WHITE,quit_button,2); screen.blit(small_font.render("Quit",True,WHITE),(quit_button.x+40,quit_button.y+10))

        elif showing_result:
            screen.blit(correct_image if is_correct else wrong_image,(0,0))

        elif showing_exit_confirm: screen.blit(exit_image,(0,0))
        elif showing_sad: screen.blit(sad_image,(0,0))

        pygame.display.flip(); clock.tick(15)

        # arm result timer once
        if showing_result and not timer_set: pygame.time.set_timer(RESULT_TIMER,3000); timer_set=True
        if not showing_result: timer_set=False

if __name__ == "__main__": main()
