# [Python pygame Game] RPG tutorial
# made by "PrintedLove"
# https://printed.tistory.com/
# https://www.youtube.com/channel/UCtKTjiof6Mwa_4ffHDYyCbQ/
#-*-coding: utf-8

import pygame, sys
from datafile import *

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

WINDOW_SIZE = (640, 480)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)    #set window size
pygame.display.set_caption('RPG tutorial')              #set window name

spr_character = SpriteSheet('spriteSheet1.png', 16, 16, 8, 8, 11)   #load Sprite Sheets

while True:     # game loop
    screen.blit(spr_character.spr[0], (320, 240))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
