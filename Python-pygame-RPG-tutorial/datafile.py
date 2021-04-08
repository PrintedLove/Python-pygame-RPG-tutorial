#-*-coding: utf-8

import pygame, os, random

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')
DIR_SOUND = os.path.join(DIR_PATH, 'sound')

WINDOW_SIZE = (640, 480)            # 창 크기
TILE_SIZE = 8                       # 타일 크기
floor_map = [-1] * int(WINDOW_SIZE[0] / TILE_SIZE / 4)     # 바닥 타일 맵(-1: 없음, 이외: y좌표)
objects = []                # 오브젝트 리스트

######

floor_map[1] = 8
floor_map[2] = 8
floor_map[3] = 8
floor_map[4] = 8
floor_map[5] = 8
floor_map[6] = 8
floor_map[7] = 8
floor_map[8] = 8

floor_map[13] = 9
floor_map[14] = 8
floor_map[15] = 8
floor_map[16] = 8
floor_map[17] = 9

######

class SpriteSheet:                      # 스프라이트 시트 클래스
    def __init__(self, filename, width, height, max_row, max_col, max_index):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename)).convert()
        self.spr = []
        self.width = width
        self.height = height

        for i in range(max_index):
            image = pygame.Surface((width, height))
            image.blit(baseImage, (0, 0), 
                       ((i % max_row) * width, (i // max_col) * height, width, height))
            image.set_colorkey((0, 0, 0))
            self.spr.append(image)

def createFloorImage(tileSpr):                                     # 바닥 타일 이미지 생성 함수
    image = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]))
    empty = True        # 빈칸
    case = 0            # 타일 타입
    spr_index = 0
    back_height = 0
    pattern_back = 0
    pattern_0 = 0

    for col in range(len(floor_map)):
        if floor_map[col] == -1:     # 비었을 경우
            empty = True
        else:                       # 타일이 존재할 경우
            if floor_map[col + 1] == -1:     # 앞 공간이 비었을 경우
                case = 2
                spr_index = 4 + random.choice([0, 2])
            else:                           # 앞 공간에 타일이 존재할 경우
                if empty == True:                   # 이전 공간이 비었을 경우
                    case = 1
                    back_height = floor_map[col]
                    spr_index = 3 + random.choice([0, 2])
                else:                               # 이전 공간에 타일이 존재할 경우
                    if floor_map[col - 1] > floor_map[col]:
                        case = 3
                        spr_index = 3 + random.choice([0, 2])
                    else:
                        if floor_map[col + 1] == floor_map[col]:
                            case = 0
                            spr_index = pattern_0
                            pattern_0 += 1

                            if pattern_0 > 2:
                                pattern_0 = 0
                        else:
                            case = 4
                            spr_index = 4 + random.choice([0, 2])

            empty = False

            # 타일 뒷부분 채우기
            for backtile in range(5 + back_height - floor_map[col]):
                if backtile < 5:
                    image.blit(tileSpr.spr[29 - 3 * backtile + pattern_back]
                               , (col * TILE_SIZE, (floor_map[col] - backtile + back_height - floor_map[col] + 4) * TILE_SIZE))
                else:
                    image.blit(tileSpr.spr[17 + pattern_back]
                               , (col * TILE_SIZE, floor_map[col] * TILE_SIZE))

            pattern_back += 1

            if pattern_back > 2:
                pattern_back = 0

            # 타일 앞부분 채우기
            image.blit(tileSpr.spr[spr_index], (col * TILE_SIZE, floor_map[col] * TILE_SIZE))

            if case == 1:
                image.blit(tileSpr.spr[12], (col * TILE_SIZE, (floor_map[col] + 1) * TILE_SIZE))
                image.blit(tileSpr.spr[13], (col * TILE_SIZE, (floor_map[col] + 2) * TILE_SIZE))
                image.blit(tileSpr.spr[9], (col * TILE_SIZE, (floor_map[col] + 3) * TILE_SIZE))
            elif case == 2:
                image.blit(tileSpr.spr[15], (col * TILE_SIZE, (floor_map[col] + 1) * TILE_SIZE))
                image.blit(tileSpr.spr[16], (col * TILE_SIZE, (floor_map[col] + 2) * TILE_SIZE))
                image.blit(tileSpr.spr[10], (col * TILE_SIZE, (floor_map[col] + 3) * TILE_SIZE))
            elif case == 3:
                image.blit(tileSpr.spr[7], (col * TILE_SIZE, (floor_map[col] + 1) * TILE_SIZE))
            elif case == 4:
                image.blit(tileSpr.spr[8], (col * TILE_SIZE, (floor_map[col] + 1) * TILE_SIZE))

    return image


class BaseObject:                       # 기본 오브젝트 클래스
    def __init__(self, spr, coord, kinds):
        self.spr = spr
        self.coord = coord
        self.width = spr.get_width()
        self.height = spr.get_height()
        self.kinds = kinds
        self.rect = pygame.rect.Rect(coord[0], coord[1], width, height)

def createObject(spr, coord, kinds):            # 오브젝트 생성 함수
    obj = BaseObject(spr, coord, kinds)
    objects.append(obj)
    return obj