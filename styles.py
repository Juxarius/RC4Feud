"""
COLOURS
"""
C_TEAL = 0, 128, 128
C_RED = 255, 0, 0
C_PINK = 255, 100, 100
C_GREEN = 0, 255, 0
C_BLUE = 0, 0, 255
C_WHITE = 255, 255, 255
C_BLACK = 0, 0, 0
C_GOLD = 255, 195, 0


"""
Questions and Answers
"""
QNA_PATH = 'QnA.txt'
with open(QNA_PATH) as f:
    data = f.read().split('\n')

getting_question = True
QUESTIONS_AND_ANSWERS = []
current_set = {}
for line in data:
    if line.startswith('#'):
        if 'q' in current_set:
            QUESTIONS_AND_ANSWERS.append(current_set.copy())
        current_set['q'] = line.strip()[1:]
        current_set['ans'] = []
    else:
        current_set['ans'].append(line)
if 'q' in current_set:
    QUESTIONS_AND_ANSWERS.append(current_set.copy())

"""
FONTS
"""
# Welcome Screen
CONFIG_WELCOME_TEXT = {
    'position': (400, 100), #Center coordinates
    'font': 'comicsans',
    'fontSize': 60,
    'text': "Welcome to RC4 Feud!!",
    'colour': C_GREEN,
}
CONFIG_START_BUTTON = {
    'position': (250, 500, 300, 50), # (topleft coordinates) x, y, width, height
    'inactiveColour': C_BLUE,
    'hoverColour': C_RED,
    'textColour': C_WHITE,
    'radius': 20,
}

# Instruction Screen
CONFIG_INSTRUCTION_TITLE = {
    'position': (400, 100), # Center coordinates
    'font': 'jokerman',
    'fontSize': 60,
    'text': "INSTRUCTIONS",
    'colour': C_PINK,
}
CONFIG_NEXT_BUTTON = {
    'position': (250, 500, 300, 50), # (topleft coordinates) x, y, width, height
    'inactiveColour': C_BLUE,
    'hoverColour': C_RED,
    'textColour': C_WHITE,
    'radius': 20,
    'text': 'Start',
}
INSTRUCTIONS = [
    "1. This game will last for 2 minutes",
    "2. You can guess the most popular answer as many times as you want",
    "3. Guessing a more popular answer will earn you more points!",
    "4. The points will be collated and awarded at the end of the game",
]
CONFIG_INSTRUCTIONS_TEXT = {
    'firstTextPosition': (100, 150), # Center coordinates
    'spaceBetweenLines': 50,
    'font': 'arial',
    'fontSize': 20,
    'colour': C_WHITE,
}

# Game Screen
CONFIG_TIMER = {
    'position': (400, 70), # Center coordinates
    'font': 'calibri',
    'fontSize': 100,
    'text': "INSTRUCTIONS",
    'colour': C_PINK,
}
CONFIG_QUESTION_TEXT = {
    'position': (400, 450), # Center coordinates
    'font': 'comicsans',
    'fontSize': 50,
    'colour': C_WHITE,
}
CONFIG_ANSWER_TEXT = {
    'font': 'comicsans',
    'fontSize': 40,
    'colour': C_PINK,
}
CONFIG_INPUT_BOX = {
    'position': (250, 500, 300, 50), # (topleft coordinates) x, y, width, height
    'radius': 10,
    'font': 'calibri',
    'fontSize': 30,
    'textColour': C_BLACK,
    'borderColour': C_BLUE,
    'borderThickness': 5,
}

# End Screen
CONFIG_END_TITLE = {
    'position': (400, 200), # Center coordinates
    'font': 'jokerman',
    'fontSize': 60,
    'colour': C_BLUE,
    'text': 'Thanks for playing!!'
}

CONFIG_FINAL_SCORE = {
    'position': (400, 300), # Center coordinates
    'font': 'arialbold',
    'fontSize': 50,
    'colour': C_RED,
}

CONFIG_FINAL_SCORE_NUM = {
    'position': (400, 370), # Center coordinates
    'font': 'calibri',
    'fontSize': 100,
    'colour': C_WHITE,
}
