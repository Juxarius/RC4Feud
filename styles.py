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
    'text': 'Start',
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
QUESTIONS_AND_ANSWERS = [
    {
        'q': "What is cold, hard and sticky?",
        'ans': ['Cum', 'A Stick', 'Frozen Glue', 'Your mom', 'Yo dad']
    },
    {
        'q': 'Question 2',
        'ans': ['answer 1', 'answer 2', 'answer 3', 'answer 4',]
    },
    {
        'q': 'Question 3',
        'ans': ['answer 1', 'answer 2', 'answer 3', 'answer 4',]
    },
]
CONFIG_TIMER = {
    'position': (400, 100), # Center coordinates
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
