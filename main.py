import pygame
import pygame_widgets as pw

"""
Content
"""
INSTRUCTIONS = [
    "1. This game will last for 2 minutes",
    "2. You can guess the most popular answer as many times as you want",
    "3. Guessing a more popular answer will earn you more points!",
    "4. The points will be collated and awarded at the end of the game",
]


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

C_TEAL = 0, 128, 128
C_RED = 255, 0, 0
C_PINK = 255, 100, 100
C_GREEN = 0, 255, 0
C_BLUE = 0, 0, 255
C_WHITE = 255, 255, 255
C_BLACK = 0, 0, 0
C_GOLD = 255, 195, 0

class Screen():
    def __init__(self, screen, next_screen=None):
        self.screen = screen
        self.next_screen = self
        self.drawings = []
        self.event_listeners = []
        self._next_screen = next_screen
    def draw(self):
        for drawing in self.drawings:
            drawing()
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
        self.start_button = pw.Button(screen, 250, 500, 300, 50, inactiveColour=C_BLUE, hoverColour=C_RED, textColour=C_WHITE,
                            text='Start', radius=20, onRelease=self.trigger_next_screen)
        self.welcome_title = pygame.font.SysFont('comicsans', 60).render("Welcome to RC4 Feud!!", True, C_GREEN)
        self.drawings = [
            lambda: self.screen.blit(self.welcome_title, self.welcome_title.get_rect(center=(400, 100))),
            self.start_button.draw,
        ]
        self.event_listeners = [
            self.start_button.listen
        ]

class InstructionScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen, GameScreen)
        self.title = pygame.font.SysFont('jokerman', 60).render('INSTRUCTIONS', True, C_PINK)
        self.next_button = pw.Button(screen, 250, 500, 300, 50, inactiveColour=C_BLUE, hoverColour=C_GREEN, textColour=C_WHITE,
                            text='Start Game!', radius=20, onRelease=self.trigger_next_screen)
        self.instruction_text = [pygame.font.SysFont('arial', 20).render(line, True, C_WHITE) for line in INSTRUCTIONS]
        def draw_instructions():
            for idx, rendered_text in enumerate(self.instruction_text):
                self.screen.blit(rendered_text, rendered_text.get_rect(topleft=(100, 150 + 50 * idx)))
        self.drawings = [
            lambda: self.screen.blit(self.title, self.title.get_rect(center=(400, 100))),
            self.next_button.draw,
            draw_instructions
        ]
        self.event_listeners = [
            self.next_button.listen,
        ]

class GameScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.time_limit = GAME_TIME_LIMIT_SECONDS + 1
        self.start_ticks = pygame.time.get_ticks()
        self.clock_font = pygame.font.SysFont('calibri', 100)
        self.question_font = pygame.font.SysFont('comicsans', 50)
        self.answer_font = pygame.font.SysFont('comicsans', 50)
        self.textbox = pw.TextBox(screen, 250, 500, 300, 50, fontSize=30,
                  borderColour=C_BLUE, textColour=C_BLACK, radius=10, placeholderText="Test", borderThickness=5)
        self.drawings = [
            self.textbox.draw,
        ]

    def draw(self):
        time_left = self.time_limit - (pygame.time.get_ticks() - self.start_ticks) / 1000
        rendered_time = self.clock_font.render(f'{int(time_left // 60)}:{int(time_left % 60):02}', True, C_WHITE)
        self.screen.blit(rendered_time, rendered_time.get_rect(center=(400, 80)))
        rendered_question = self.question_font.render(self.get_question(), True, C_WHITE)
        self.screen.blit(rendered_question, rendered_question.get_rect(center=(400, 150)))
        for i in range(8):
            self.draw_answer_frame((CONSOLE_WIDTH / 2 + (-305 if i % 2 == 0 else 5), 200 + i//2 * 60))
        super().draw()

    def draw_answer_frame(self, topleft):
        w, h = 300, 50
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

    def get_question(self):
        return "What is cold, hard and sticky?"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print(self.textbox.getText())
        self.textbox.listen(events)
        super().handle_events(events)


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
