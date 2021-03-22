#-*-coding: utf-8

import pygame, os

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')
DIR_SOUND = os.path.join(DIR_PATH, 'sound')

class SpriteSheet:
    def __init__(self, filename, width, height, max_row, max_col, max_index):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename)).convert()
        self.spr = []

        for i in range(max_index):
            image = pygame.Surface((width, height))
            image.blit(baseImage, (0, 0), 
                       ((i % width) * width, (i / max_row) * height, width, height))
            image_scaled = pygame.transform.scale(image, (width * 4, height * 4))
            self.spr.append(image_scaled)