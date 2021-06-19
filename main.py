import pygame
import pygame_widgets as pw
from styles import *
import random

"""
GLOBALS
"""
CONSOLE_WIDTH = 800
CONSOLE_HEIGHT = 600
CONSOLE_SIZE = (CONSOLE_WIDTH, CONSOLE_HEIGHT)
CONSOLE_TITLE = "RC4 FEUD"
FPS = 60
GAME_TIME_LIMIT_SECONDS = 120


"""
STATICS
"""
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode(CONSOLE_SIZE)
pygame.display.set_caption(CONSOLE_TITLE)


class Screen():
    def __init__(self, screen, next_screen=None):
        self.screen = screen
        self.next_screen = self
        self.drawings = []
        self.event_listeners = []
        self._next_screen = next_screen
    def draw(self):
        for drawing in self.drawings:
            try:
                drawing()
            except Exception as e:
                pass # weirdest buggy issue with textbox code, requires this except
    def handle_events(self, events):
        for event_listener in self.event_listeners:
            event_listener(events)
    def trigger_next_screen(self):
        self.next_screen = self._next_screen(self.screen)
    def set_next_screen(self, screen):
        self._next_screen = screen
    def get_next_screen(self):
        return self.next_screen

class WelcomeScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen, InstructionScreen)
        cwt = CONFIG_WELCOME_TEXT
        self.start_button = Button(screen, *CONFIG_START_BUTTON['position'], text='Start', **CONFIG_START_BUTTON, onRelease=self.trigger_next_screen)
        self.welcome_title = pygame.font.SysFont(cwt['font'], cwt['fontSize']).render(cwt['text'], True, cwt['colour'])
        self.drawings = [
            lambda: self.screen.blit(self.welcome_title, self.welcome_title.get_rect(center=cwt['position'])),
            self.start_button.draw,
        ]
        self.event_listeners = [
            self.start_button.listen
        ]

class InstructionScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen, GameScreen)
        cit = CONFIG_INSTRUCTION_TITLE
        self.title = pygame.font.SysFont(cit['font'], cit['fontSize']).render(cit['text'], True, cit['colour'])
        self.next_button = Button(screen, *CONFIG_NEXT_BUTTON['position'], **CONFIG_NEXT_BUTTON, onRelease=self.trigger_next_screen)
        cit = CONFIG_INSTRUCTIONS_TEXT
        self.instruction_text = [pygame.font.SysFont(cit['font'], cit['fontSize']).render(line, True, cit['colour']) for line in INSTRUCTIONS]
        ftpx, ftpy = cit['firstTextPosition']
        def draw_instructions():
            for idx, rendered_text in enumerate(self.instruction_text):
                self.screen.blit(rendered_text, rendered_text.get_rect(topleft=(ftpx, ftpy + cit['spaceBetweenLines'] * idx)))
        self.drawings = [
            lambda: self.screen.blit(self.title, self.title.get_rect(center=CONFIG_INSTRUCTION_TITLE['position'])),
            self.next_button.draw,
            draw_instructions
        ]
        self.event_listeners = [
            self.next_button.listen,
        ]

class GameScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen, EndScreen)
        self.curr_q, self.curr_a, self.curr_revealed, self.score = '', [], [], 0
        self.qna = QUESTIONS_AND_ANSWERS
        self.get_next_question()
        self.time_limit = GAME_TIME_LIMIT_SECONDS + 1
        self.start_ticks = pygame.time.get_ticks()
        self.clock_font = pygame.font.SysFont(CONFIG_TIMER['font'], CONFIG_TIMER['fontSize'])
        self.question_font = pygame.font.SysFont(CONFIG_QUESTION_TEXT['font'], CONFIG_QUESTION_TEXT['fontSize'])
        self.answer_font = pygame.font.SysFont(CONFIG_ANSWER_TEXT['font'], CONFIG_ANSWER_TEXT['fontSize'])
        cib = CONFIG_INPUT_BOX
        cib['font'] = pygame.font.SysFont(cib['font'], cib['fontSize'])
        self.textbox = pw.TextBox(screen, *cib['position'], onSubmit=self.process_answer, **cib)
        self.drawings = [
            self.textbox.draw,
        ]

    def draw(self):
        time_left = self.time_limit - (pygame.time.get_ticks() - self.start_ticks) / 1000
        rendered_time = self.clock_font.render(f'{int(time_left // 60)}:{int(time_left % 60):02}', True, CONFIG_TIMER['colour'])
        self.screen.blit(rendered_time, rendered_time.get_rect(center=CONFIG_TIMER['position']))
        rendered_question = self.question_font.render(self.curr_q, True, CONFIG_QUESTION_TEXT['colour'])
        self.screen.blit(rendered_question, rendered_question.get_rect(center=CONFIG_QUESTION_TEXT['position']))

        for idx, ans in enumerate(self.curr_a):
            if not self.curr_revealed[idx]:
                ans = ''
            self.draw_answer_frame(topleft=(CONSOLE_WIDTH / 2 + (-305 if idx % 2 == 0 else 5), 130 + idx//2 * 60), text=ans)
        super().draw()

        if time_left < 0:
            self.trigger_next_screen()

    def draw_answer_frame(self, topleft=None, center=None, text=''):
        w, h = 300, 50
        if not topleft:
            topleft = center[0] - w/2, center[1] - h/2
        if not center:
            center = topleft[0] + w/2, topleft[1] + h/2
        x, y = topleft
        cutoff = 5
        coords = [
            (x+cutoff, y),
            (x+w-cutoff, y),
            (x+w, y+cutoff),
            (x+w, y+h-cutoff),
            (x+w-cutoff, y+h),
            (x+cutoff, y+h),
            (x, y+h-cutoff),
            (x, y+cutoff)
        ]
        pygame.draw.lines(self.screen, C_GOLD, True, coords, width=4)
        if text:
            rendered_text = self.answer_font.render(text, True, C_WHITE)
            self.screen.blit(rendered_text, rendered_text.get_rect(center=center))

    def get_next_question(self):
        try:
            random_q = self.qna.pop(random.randrange(len(self.qna) - 1))
            self.curr_q, self.curr_a = random_q['q'], random_q['ans']
            self.curr_revealed = [False] * len(self.curr_a)
        except Exception as e:
            self.curr_q, self.curr_a, self.curr_revealed = '', [], []

    def process_answer(self):
        input = self.textbox.getText()
        self.textbox.setText('')
        for idx, ans in enumerate(self.curr_a):
            ans = ' '.join(ans.split()[:-1])
            exact_match = input.lower().strip() == ans.lower().strip()
            word_match = any(input_word in ans.lower().split() for input_word in input.lower().split())
            matches = [exact_match]
            if any(matches):
                self.curr_revealed[idx] = True
        if all(self.curr_revealed):
            self.score += 1
            self.get_next_question()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print(self.textbox.getText())
        self.textbox.listen(events)
        super().handle_events(events)

    def trigger_next_screen(self):
        self.next_screen = EndScreen(self.screen, self.score)


class EndScreen(Screen):
    def __init__(self, screen, score):
        super().__init__(screen)
        cet = CONFIG_END_TITLE
        self.title = pygame.font.SysFont(cet['font'], cet['fontSize']).render(cet['text'], True, cet['colour'])
        cfs = CONFIG_FINAL_SCORE
        self.score_text = pygame.font.SysFont(cfs['font'], cfs['fontSize']).render('Final Score:', True, cfs['colour'])
        cfsn = CONFIG_FINAL_SCORE_NUM
        self.score_num = pygame.font.SysFont(cfsn['font'], cfsn['fontSize']).render(str(score), True, cfsn['colour'])
        self.drawings = [
            lambda: self.screen.blit(self.title, self.title.get_rect(center=cet['position'])),
            lambda: self.screen.blit(self.score_text, self.score_text.get_rect(center=cfs['position'])),
            lambda: self.screen.blit(self.score_num, self.score_num.get_rect(center=cfsn['position'])),
        ]

class Button:
    def __init__(self, screen, x, y, w, h, text='', onRelease=None, inactiveColour=C_BLUE, hoverColour=C_BLUE, textColour=C_WHITE, radius=0, *args, **kwargs):
        self.screen = screen
        self.position = x, y, w, h
        self.text = pygame.font.SysFont('calibri', 30).render(text, True, textColour)
        self.onRelease = onRelease
        self.inactiveColour = inactiveColour
        self.hoverColour = hoverColour
        self.textColour = textColour
        self.radius = radius
        self.center = x + w // 2, y + h // 2

    def draw(self):
        pygame.draw.rect(self.screen, self.inactiveColour, self.position, border_radius=self.radius)
        if pygame.Rect(*self.position).collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, self.hoverColour, self.position, border_radius=self.radius)
        self.screen.blit(self.text, self.text.get_rect(center=self.center))

    def listen(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and pygame.Rect(*self.position).collidepoint(pygame.mouse.get_pos()):
                self.onRelease()
        

def main():
    clock = pygame.time.Clock()
    current_screen = WelcomeScreen(screen)
    running = True
    while running:
        clock.tick(FPS)
        screen.fill(C_TEAL)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        current_screen.handle_events(events)
        current_screen.draw()
        pygame.display.update()
        current_screen = current_screen.get_next_screen()
    pygame.quit()

if __name__ == '__main__':
    main()
