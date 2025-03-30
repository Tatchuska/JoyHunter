MENU_OPTION = ('START GAME',
               'EXIT')
# Define Game variables
FPS = 60
GRAVITY = 0.6
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 324
SCROLL_LIMIT = 200
TILE_SIZE = 30
screen_scroll = 0
bg_scroll = 0
ground_height = 92
enemy_y = SCREEN_HEIGHT - ground_height
start_game = False
bark_trigger = False

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 102, 0)
LIGHT_GREEN = (0, 204, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)

# Create list of positions for the crystals
crystal_data = [
    ("Blue", 350, 150),
    ("Blue", 400, 125),
    ("Yellow", 450, 100),
    ("Blue", 500, 125),
    ("Blue", 550, 150),
    ("Blue", 800, 120),
    ("Blue", 850, 100),
    ("Yellow", 900, 80),
    ("Blue", 950, 100),
    ("Blue", 1000, 120),
    ("Blue", 1200, 150),
    ("Blue", 1225, 125),
    ("Red", 1250, 100),
    ("Blue", 1275, 125),
    ("Blue", 1300, 150),
    ("Blue", 1500, 150),
    ("Blue", 1550, 125),
    ("Yellow", 1600, 100),
    ("Blue", 1650, 125),
    ("Blue", 1700, 150),
    ("Blue", 2000, 150),
    ("Blue", 2025, 125),
    ("Yellow", 2050, 100),
    ("Blue", 2075, 125),
    ("Blue", 2100, 150),
    ("Blue", 2400, 150),
    ("Blue", 2450, 125),
    ("Yellow", 2500, 100),
    ("Blue", 2550, 125),
    ("Blue", 2600, 150),
]

# Create list of positions for the enemies
enemy_data = [
    ('Dog', 400, enemy_y, 1.5, 2),
    ('Dog', 1050, enemy_y, 1.5, 2),
    ('Dog', 1800, enemy_y, 1.5, 2),
    ('Dog', 2300, enemy_y, 1.5, 2),
    ('Dog', 2450, enemy_y, 1.5, 2),
    ('Hound', 800, enemy_y, 1.75, 3),
    ('Hound', 1250, enemy_y, 1.75, 3),
    ('Hound', 2050, enemy_y, 1.75, 3),
]