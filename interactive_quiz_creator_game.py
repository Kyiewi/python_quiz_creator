#Import necessary modules
import sys
import pygame
from pygame.constants import USEREVENT
from pygame.locals import *

#initialize pygame and mixer(for sound)
pygame.init()
pygame.mixer.init()

#Setup Display
WIDTH, HEIGHT = 1060, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Game")

#Font
font = pygame.font.SysFont("Courier", 25)
small_font = pygame.font.SysFont("Courier", 20)

#Color
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)

#For easier load and scale images
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

#---------------INPUTBOX CLASS--------------

class InputBox:
    def __init__(self, x, y, w, h, text='', dynamic_width=True, editable=True):
        #rectangle area for input box
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.txt_surface = font.render(text, True, WHITE)
        self.active = False
        self.dynamic_width = dynamic_width
        self.editable = editable

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
            self.rect.w = self.txt_surface.get_width() + 10

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

answer_input = InputBox(427,368,80,40, dynamic_width=False, editable=True)

# -----------------BUTTONS--------------------
create_button = pygame.Rect(319, 320, 200, 50)
play_button = pygame.Rect(319, 390, 200, 50)
enter_button = pygame.Rect(201, 470, 150, 50)
quit_button = pygame.Rect(500, 470, 150, 50)
submit_button = pygame.Rect(201, 470, 150, 50)
back_button = pygame.Rect(500, 400, 150, 50)
yes_button = pygame.Rect(152, 371, 190, 65)
no_button = pygame.Rect(494, 371, 190, 65)

# State flags
showing_start        = True
showing_loading      = False
showing_create       = False
showing_exit_confirm = False
showing_sad          = False
showing_answer       = False
showing_result       = False

timer_set           = False
saved_msg           = ''
save_time           = 0
is_correct          = False
current_question    = []

# Load a random question
def load_random_question():
    try:
        with open("quiz_data.txt") as f:
            parts = f.read().strip().split("Number:")
            question_blocks = [p for p in parts if p.strip()]
            chosen = random.choice(question_blocks)
            return chosen.splitlines()
    except Exception:
        return []

# Draw back & quit
def draw_back_and_quit():
    pygame.draw.rect(screen, WHITE, back_button, 2)
    screen.blit(small_font.render("Back", True, WHITE),(back_button.x+40, back_button.y+10))
    pygame.draw.rect(screen, WHITE, quit_button, 2)
    screen.blit(small_font.render("Quit", True, WHITE),(quit_button.x+40, quit_button.y+10))

#Main functions
def main():
    global showing_start, showing_loading, showing_create, showing_exit_confirm
    global showing_sad, showing_answer, showing_result, timer_set
    global saved_msg, save_time, is_correct, current_question

    clock = pygame.time.Clock()
    loading_frame = start_frame = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                # Start menu
                if showing_start:
                    if create_button.collidepoint(event.pos):
                        click_sound.play(); showing_start=False; showing_loading=True; load_frame=0
                    elif play_button.collidepoint(event.pos):
                        click_sound.play(); current_question=load_random_question();
                        for i,line in enumerate(current_question[:6]):
                            if ':' in line: boxes[i].set_text(line.split(':',1)[1].strip())
                        answer_input.clear(); showing_start=False; showing_answer=True

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

        screen.fill((0, 0, 0))

        if showing_start:
            screen.blit(start_images[start_frame], (0, 0))
            pygame.time.delay(80) #to delay start images a lil bit
            start_frame = (start_frame +1) %len(start_images)

        elif showing_loading:
            if loading_frame < len(loading_images):
                screen.blit(loading_images[loading_frame], (0, 0))
                pygame.time.delay(120) #to delay loading images since it's too fast
                loading_frame += 1
            else:
                showing_loading = False #close after animation
                showing_start = True

        elif showing_start:
            screen.blit(quiz_template, (0, 0)) #show background image

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

        elif showing_sad:
            screen.blit(sad_image, (0, 0))  # show background image

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()