#-*-coding: utf-8

import pygame, os, random

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')
DIR_SOUND = os.path.join(DIR_PATH, 'sound')

WINDOW_SIZE = (960, 640)            # 창 크기
TILE_SIZE = 8                       # 타일 크기
floor_map = [-1] * int(WINDOW_SIZE[0] / TILE_SIZE / 4)     # 바닥 타일 맵(-1: 없음, 이외: y좌표)

objects = []                # 오브젝트 리스트

###### 테스트용 바닥 타일 리스트
floor_map[1] = 14
floor_map[2] = 13
floor_map[3] = 13
floor_map[4] = 13
floor_map[5] = 13
floor_map[6] = 13
floor_map[7] = 13
floor_map[8] = 13

floor_map[12] = 10
floor_map[13] = 9
floor_map[14] = 9
floor_map[15] = 9
floor_map[16] = 10

floor_map[18] = 11
floor_map[19] = 10
floor_map[20] = 10
floor_map[21] = 10
floor_map[22] = 10
floor_map[23] = 11
floor_map[24] = 11
floor_map[25] = 11
floor_map[26] = 11
floor_map[27] = 11
floor_map[28] = 12
######

# 스프라이트 시트 클래스
class SpriteSheet:           
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

# 기본 오브젝트 클래스
class BaseObject:
    def __init__(self, spr, coord, kinds):
        self.spr = spr
        self.coord = coord
        self.width = spr.get_width()
        self.height = spr.get_height()
        self.kinds = kinds
        self.rect = pygame.rect.Rect(coord[0], coord[1], width, height)

# 오브젝트 생성 함수
def createObject(spr, coord, kinds):            
    obj = BaseObject(spr, coord, kinds)
    objects.append(obj)
    return obj

# 바닥 타일 이미지 생성 함수
def createMapImage(tileSpr):
    image = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]))
    empty = True                        # 빈칸
    case = 0                            # 타일 타입
    spr_index, spr_index2 = 0, []       # 타일 스프라이트 인덱스
    back_height = 0
    pattern_back = 0
    pattern_0 = 0

    for col in range(len(floor_map)):
        if floor_map[col] == -1:     # 비었을 경우
            empty = True
        else:                        # 타일이 존재할 경우
            if floor_map[col + 1] == -1:     # 앞 공간이 비었을 경우
                case = 2
                spr_index, spr_index2 = 4 + random.choice([0, 2]), [15, 16, 10]
            else:                           # 앞 공간에 타일이 존재할 경우
                if empty == True:                   # 이전 공간이 비었을 경우
                    case = 1
                    back_height = floor_map[col]
                    spr_index, spr_index2 = 3 + random.choice([0, 2]), [12, 13, 9]
                else:                               # 이전 공간에 타일이 존재할 경우
                    if floor_map[col - 1] > floor_map[col]:
                        case = 3
                        spr_index, spr_index2 = 3 + random.choice([0, 2]), [7]
                    else:
                        if floor_map[col + 1] == floor_map[col]:
                            case = 0
                            spr_index = pattern_0
                            pattern_0 += 1

                            if pattern_0 > 2:
                                pattern_0 = 0
                        else:
                            case = 4
                            spr_index, spr_index2 = 4 + random.choice([0, 2]), [8]
            empty = False

            for backtile in range(5 + back_height - floor_map[col]):        # 타일 뒷부분 채우기
                if backtile < 5:
                    image.blit(tileSpr.spr[29 - 3 * backtile + pattern_back], (col * TILE_SIZE
                        , (floor_map[col] - backtile + back_height - floor_map[col] + 4) * TILE_SIZE))
                else:
                    image.blit(tileSpr.spr[17 + pattern_back], (col * TILE_SIZE
                        , floor_map[col] * TILE_SIZE))
            pattern_back += 1

            if pattern_back > 2:
                pattern_back = 0

            image.blit(tileSpr.spr[spr_index], (col * TILE_SIZE, floor_map[col] * TILE_SIZE))   # 타일 앞부분 채우기

            if case != 0:
                i = 0
                for spr_indexs in spr_index2:
                    i += 1
                    image.blit(tileSpr.spr[spr_indexs], (col * TILE_SIZE, (floor_map[col] + i) * TILE_SIZE))
    return image