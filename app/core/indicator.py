import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from .path import get_path

pygame.mixer.init()
sound = pygame.mixer.Sound(get_path('app/static/sounds/beep.wav'))

async def beep():
    sound.play()
