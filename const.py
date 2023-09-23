# Constants
import os

import pygame


COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'violet': (143, 0, 255)
}

WS_RESOLUTIONS = {
    '3840x2160 (4K UHD)': (3840, 2160),
    '2560x1440 (2K WQHD)': (2560, 1440),
    '1920x1080 (Full-HD)': (1920, 1080),
    '1600x900': (1600, 900),
    '1366x768': (1366, 768),
    '1280x720 (HD)': (1280, 720),
}

# old
WIDTH, HEIGHT = 1600, 900 # need to remove using game_data
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space_bg.webp')), (WIDTH, HEIGHT))
MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'main_menu.webp')), (WIDTH, HEIGHT))
