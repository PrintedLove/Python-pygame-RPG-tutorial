#-*-coding: utf-8

import pygame, os

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')
DIR_SOUND = os.path.join(DIR_PATH, 'sound')

objects = []        # 오브젝트 리스트

class TileType:
    def __init__(self, tile_index):
        self.tile_type = tile_index

class SpriteSheet:                      # 스프라이트 시트 클래스
    def __init__(self, filename, width, height, max_row, max_col, max_index):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename)).convert()
        self.spr = []
        self.width = width
        self.height = height

        for i in range(max_index):
            image = pygame.Surface((width, height))
            image.blit(baseImage, (0, 0), 
                       ((i % width) * width, (i / max_row) * height, width, height))
            image.set_colorkey((0, 0, 0))
            self.spr.append(image)

class BaseObject:                       # 기본 오브젝트 클래스
    def __init__(self, spr, width, height, coord, kinds):
        self.spr = spr
        self.coord = coord
        self.width = width
        self.height = height
        self.kinds = tile_kinds
        self.rect = pygame.rect.Rect(coord[0], coord[1], width, height)

def createObject(coord, kinds):            # 타일 생성 함수
    if kinds < 100:
        spr = 1

    newObject = BaseObject(spr, width, height, coord, kinds)
    objects.append(newObject)