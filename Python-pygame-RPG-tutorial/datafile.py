#-*-coding: utf-8

import pygame, os, random

DIR_PATH = os.path.dirname(__file__)    # 파일 위치
DIR_IMAGE = os.path.join(DIR_PATH, 'image')
DIR_SOUND = os.path.join(DIR_PATH, 'sound')
DIR_FONT = os.path.join(DIR_PATH, 'font')

WINDOW_SIZE = (960, 640)            # 창 크기
TILE_SIZE = 8                       # 타일 크기
TILE_MAPSIZE = (int(WINDOW_SIZE[0] / 7.5), int(WINDOW_SIZE[1] / 20))

BACKGROUND_COLOR = (27, 25, 25)

DEFAULT_FONT_NAME = "munro.ttf"

floor_map = [-1] * TILE_MAPSIZE[0]     # 바닥 타일 맵(-1: 없음, 이외: y좌표)

objects = []                # 오브젝트 리스트
enemys = []                 # 적 오브젝트 리스트

# 스프라이트 시트 클래스 
class SpriteSheet:           
    def __init__(self, filename, width, height, max_row, max_col, max_index):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename)).convert()
        self.spr = []
        self.width = width
        self.height = height

        for i in range(max_index):      # 스프라이트 시트의 각 인덱스에 자른 이미지 저장
            image = pygame.Surface((width, height))
            image.blit(baseImage, (0, 0), 
                       ((i % max_row) * width, (i // max_col) * height, width, height))
            image.set_colorkey((0, 0, 0))
            self.spr.append(image)

# 스프라이트 세트 생성 함수 
def createSpriteSet(spriteSheet, index_list, index_max = None):
    spr = []

    if index_max == None:
        for index in index_list:
            spr.append(spriteSheet.spr[index])
    else:
        for index in range(index_list, index_max + 1):
            spr.append(spriteSheet.spr[index])

    return spr

# 텍스트 드로우 함수
def draw_text(screen, text, size, color, x, y):
    gameFont = pygame.font.Font(os.path.join(DIR_FONT, DEFAULT_FONT_NAME), size)
    text_surface = gameFont.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (round(x), round(y))
    screen.blit(text_surface, text_rect)

# 기본 오브젝트 클래스
class BaseObject:
    def __init__(self, spr, coord, kinds, game):
        self.kinds = kinds
        self.spr = spr
        self.spr_index = 0
        self.game = game
        self.width = spr[0].get_width()
        self.height = spr[0].get_height()
        self.direction = True
        self.vspeed = 0
        self.gravity = 0.2
        self.movement = [0, 0]
        self.collision = {'top' : False, 'bottom' : False, 'right' : False, 'left' : False}
        self.rect = pygame.rect.Rect(coord[0], coord[1], self.width, self.height)
        self.frameSpeed = 0
        self.frameTimer = 0
        self.destroy = False

    def physics(self):
        self.movement[0] = 0
        self.movement[1] = 0

        if self.gravity != 0:
            self.movement[1] += self.vspeed

            self.vspeed += self.gravity
            if self.vspeed > 3:
                self.vspeed = 3

    def physics_after(self):
        self.rect, self.collision = move(self.rect, self.movement)

        if self.collision['bottom']:
            self.vspeed = 0

        if self.rect.y > 400 or self.rect.y  > 400 or self.rect.y  > 400:
            self.destroy = True
    
    def draw(self):
        self.game.screen_scaled.blit(pygame.transform.flip(self.spr[self.spr_index], self.direction, False)
                    , (self.rect.x - self.game.camera_scroll[0], self.rect.y - self.game.camera_scroll[1]))

        if self.kinds == 'enemy' and self.hp < self.hpm:
            pygame.draw.rect(self.game.screen_scaled, (131, 133, 131)
            , [self.rect.x - 1 - self.game.camera_scroll[0], self.rect.y - 5 - self.game.camera_scroll[1], 10, 2])
            pygame.draw.rect(self.game.screen_scaled, (189, 76, 49)
            , [self.rect.x - 1 - self.game.camera_scroll[0], self.rect.y - 5 - self.game.camera_scroll[1], 10 * self.hp / self.hpm, 2])

    def animation(self, mode):
        if mode == 'loop':
            self.frameTimer += 1

            if self.frameTimer >= self.frameSpeed:
                self.frameTimer = 0
                if self.spr_index < len(self.spr) - 1:
                    self.spr_index += 1
                else:
                    self.spr_index = 0

    def destroy_self(self):
        if self.kinds == 'enemy':
            enemys.remove(self)

        objects.remove(self)
        del(self)

# 적 오브젝트 클래스
class EnemyObject(BaseObject):
    def __init__(self, spr, coord, kinds, game, types):
        super().__init__(spr, coord, kinds, game)
        self.types = types
        self.actSpeed = 0
        self.actTimer = 0
        self.hpm = 0
        self.hp = 0

    def events(self):
        if self.hp < 1:
            self.destroy = True
            self.game.sound_monster.play()

            for i in range(4):
                coin = createObject(self.game.spr_coin, (self.rect.x + random.randrange(-3, 4), self.rect.y - 2), 'coin', self.game)
                coin.vspeed = random.randrange(-3, 0)
                coin.direction = random.choice([True, False])

        if self.destroy == False:
            self.physics()

            if self.types == 'snake':       # 뱀일 경우
                self.animation('loop')

                if self.direction == False:
                    if floor_map[self.rect.right // TILE_SIZE] != -1:
                        self.movement[0] += 1
                    else:
                        self.direction = True
                else:
                    if floor_map[self.rect.right // TILE_SIZE - 1] != -1:
                        self.movement[0] -= 1
                    else:
                        self.direction = False
            elif self.types == 'slime':       # 슬라임일 경우
                self.actTimer += 1
                self.frameTimer += 1

                if self.vspeed >= 0:
                    if self.frameTimer >= self.frameSpeed:
                        self.frameTimer = 0
                        if self.spr_index == 0:
                            self.spr_index = 1
                        else:
                            self.spr_index = 0
                else:
                    self.spr_index = 2

                if self.actTimer == self.actSpeed - 35:
                    self.vspeed = -3
                elif self.actTimer > self.actSpeed:
                    self.actTimer = 0
                elif self.actTimer > self.actSpeed - 35:
                    if self.game.player_rect.x - self.rect.x > 0:
                        if floor_map[self.rect.right // TILE_SIZE] != -1:
                            self.direction = False
                            self.movement[0] += 1
                    else:
                        if floor_map[self.rect.right // TILE_SIZE - 1] != -1:
                            self.direction = True
                            self.movement[0] -= 1

            if self.collision['right'] or self.collision['left']:
                self.vspeed = -2

# 투사체 오브젝트 클래스
class EffectObject(BaseObject):
    def __init__(self, spr, coord, kinds, game, types):
        super().__init__(spr, coord, kinds, game)
        self.types = types
        self.lifetime = 0
        self.lifeTimer = 0
        self.damage = 0

    def events(self):
        self.physics()
        self.lifeTimer += 1

        if self.lifeTimer > self.lifetime:
            self.destroy = True

        if self.types == 'player_shot':       # 플레이어 공격일 경우
            self.animation('loop')

            if self.direction == False:
                self.movement[0] += 3
            else:
                self.movement[0] -= 3

            if self.collision['right'] or self.collision['left']:
                if self.direction:
                    self.direction = False
                    self.movement[0] += 4
                else:
                    self.direction = True
                    self.movement[0] -= 4

            for enemy in enemys:            # 적과 충돌 계산
                if self.destroy == False and enemy.destroy == False and self.rect.colliderect(enemy.rect):
                    self.destroy = True
                    enemy.hp -= self.damage

# 아이템 오브젝트 클래스
class ItemObject(BaseObject):
    def __init__(self, spr, coord, kinds, game, types):
        super().__init__(spr, coord, kinds, game)
        self.types = types

    def events(self):
        self.physics()
        self.animation('loop')

        if self.direction == False:
            self.movement[0] += 1
        else:
            self.movement[0] -= 1

        if self.collision['right'] or self.collision['left']:
            if self.direction:
                self.direction = False
                self.movement[0] += 2
            else:
                self.direction = True
                self.movement[0] -= 2

        if self.destroy == False and self.rect.colliderect(self.game.player_rect):
            self.destroy = True
            self.game.gameScore += 5
            self.game.sound_coin.play()


# 오브젝트 생성 함수
def createObject(spr, coord, types, game):
    if types == 'snake':
        obj = EnemyObject(spr, coord, 'enemy', game, types)
        obj.hpm = 50
        obj.hp = obj.hpm
        obj.frameSpeed = 4
    if types == 'slime':
        obj = EnemyObject(spr, coord, 'enemy', game, types)
        obj.hpm = 100
        obj.hp = obj.hpm
        obj.frameSpeed = 12
        obj.actSpeed = 120
        obj.actTimer = random.randrange(0, 120)
    if types == 'player_shot':
        obj = EffectObject(spr, coord, 'effect', game, types)
        obj.frameSpeed = 10
        obj.lifetime = 100
        obj.vspeed = -1
        obj.damage = 30
    if types == 'coin':
        obj = ItemObject(spr, coord, 'item', game, types)
        obj.frameSpeed = 25

    objects.append(obj)

    if obj.kinds == 'enemy':
        enemys.append(obj)

    return obj

# 바닥과 충돌 검사 함수
def collision_floor(rect):
    hit_list = []
    col = 0

    for row in floor_map:
        if row != -1:
            floor_rect = pygame.rect.Rect((col * TILE_SIZE, row * TILE_SIZE), (TILE_SIZE, TILE_SIZE * 5))
            if rect.colliderect(floor_rect):
                hit_list.append(floor_rect)
        col += 1

    return hit_list

# 오브젝트 이동 함수
def move(rect, movement):
    collision_types = {'top' : False, 'bottom' : False, 'right' : False, 'left' : False}    # 충돌 타입
    rect.x += movement[0]
    hit_list = collision_floor(rect)

    for tile in hit_list:           # X축 충돌 리스트 갱신
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_floor(rect)

    for tile in hit_list:           # Y축 충돌 리스트 갱신
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types

# 맵 데이터 생성 함수
def createMapData():
    ground_baseheight = 16      # 기본 바닥 높이
    ground_interval = 0         # 바닥 간 간격
    ground_maxsize = random.randrange(13, 24)        # 바닥 최대 크기
    ground_maxsize_count = 0
    ground_size = random.randrange(2, 5)             # 바닥 단위 크기
    ground_size_count = 0
    ground_height = ground_baseheight + random.randrange(-2, 3)           # 바닥 높이
    ground_heightChange = 0
    ground_mode_stack = 1       # 큰 크기 스택 (큰 크기 1~4개 생성 후 작은 크기 1개 생성)
    ground_mode_stackMax = random.randrange(2, 6)

    for i in range(TILE_MAPSIZE[0] - 1):
        if ground_interval > 0:         # 바닥 간격 띄우기
            floor_map[i] = -1
            ground_interval -= 1
        else:
            if ground_maxsize_count < ground_maxsize:
                if ground_size_count < ground_size:
                    if ground_maxsize_count == 0 and ground_size > 2:                     # 바닥 시작 처리
                        floor_map[i] = ground_height + ground_heightChange + random.choice([0, 1])
                        ground_size_count += 1
                    else:
                        floor_map[i] = ground_height + ground_heightChange
                        ground_size_count += 1
                else:
                    if ground_maxsize_count == ground_maxsize - 1:      # 바닥 끝 처리
                        if floor_map[i - 2] == floor_map[i - 1]:
                            floor_map[i] = ground_height + ground_heightChange + random.choice([0, 1])
                        else:
                            floor_map[i] = floor_map[i - 1]

                        ground_size_count += 1
                    else:
                        ground_size_count = 0
                        ground_size = random.randrange(2, 5)
                        ground_heightChange += random.choice([0, 1])
                        
                        if abs(ground_heightChange) > 2:
                            ground_heightChange -= ground_heightChange // 3

                        floor_map[i] = ground_height + ground_heightChange

                ground_maxsize_count += 1
            else:               # 바닥 완성시 다음 바닥 크기 및 간격 크기 처리
                if ground_mode_stack < ground_mode_stackMax:    # 큰 크기
                    ground_mode_stack += 1

                    if ground_mode_stack == 1:
                        ground_interval = random.randrange(2, 6)
                    else:
                        ground_interval = random.randrange(1, 4)

                    ground_maxsize = random.randrange(13, 25)
                    ground_size = random.randrange(2, 9)
                else:                                           # 작은 크기
                    ground_mode_stack = 0
                    ground_mode_stackMax = random.randrange(2, 6)
                    ground_interval = random.randrange(2, 6)
                    ground_maxsize = random.randrange(4, 9)
                    ground_size = random.randrange(2, 5)

                ground_height = ground_baseheight + random.randrange(-1, 1)
                ground_heightChange = 0
                ground_maxsize_count = 0
                ground_size_count = 0

# 맵 이미지 생성 함수
def createMapImage(tileSpr, structSpr):
    image = pygame.Surface((TILE_MAPSIZE[0] * 8, TILE_MAPSIZE[1] * 8))
    front_image = pygame.Surface((TILE_MAPSIZE[0] * 8, TILE_MAPSIZE[1] * 8))
    empty = True                        # 빈칸
    case = 0                            # 타일 타입
    spr_index, spr_index2 = 0, []       # 타일 스프라이트 인덱스
    back_height = 0
    pattern_back = 0
    pattern_0 = 0

    for col in range(TILE_MAPSIZE[0] - 1):
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

            # 구조물 채우기
            if random.randrange(0, 100) <= 4 and case == 0:
                if random.choice([True, False]):
                    image.blit(tileSpr.spr[32], ((col) * TILE_SIZE, (floor_map[col] - 1) * TILE_SIZE))
                else:
                    image.blit(tileSpr.spr[35], ((col - 1) * TILE_SIZE, (floor_map[col] - 2) * TILE_SIZE))
                    image.blit(tileSpr.spr[36], ((col) * TILE_SIZE, (floor_map[col] - 2) * TILE_SIZE))
                    image.blit(tileSpr.spr[37], ((col - 1) * TILE_SIZE, (floor_map[col] - 1) * TILE_SIZE))
                    image.blit(tileSpr.spr[38], ((col) * TILE_SIZE, (floor_map[col] - 1) * TILE_SIZE))

            if random.randrange(0, 100) <= 14:
                struct_types = random.choice(['leaf', 'flower', 'obj', 'sign', 'gravestone', 'skull'])
                struct_index = random.randrange(structSpr[struct_types][0], structSpr[struct_types][1])
                front_image.blit( tileSpr.spr[struct_index], (col * TILE_SIZE, (floor_map[col] - 1) * TILE_SIZE))

            if random.choice([True, False]):
                struct_index = random.randrange(47, 55)
                front_image.blit(tileSpr.spr[struct_index], (col * TILE_SIZE, (floor_map[col] - 1) * TILE_SIZE)) 

    image.set_colorkey((0, 0, 0))
    front_image.set_colorkey((0, 0, 0))

    return image, front_image

# 배경 이미지 생성함수
def createBackImage(tileSpr):
    image = pygame.Surface((int(WINDOW_SIZE[0] / 2), int(WINDOW_SIZE[1] / 12)))

    for row in range(16):
        for col in range(4):
            star_case = random.randrange(-(col + 2), 3)

            if star_case >= 0:
                image.blit(tileSpr.spr[random.randrange(0, 31)]
                           , (row * TILE_SIZE * 2 + random.randrange(-4, 5)
                            , col * TILE_SIZE * 2 + random.randrange(-4, 5)))

    image.blit(tileSpr.spr[31], (24 * TILE_SIZE, 2 * TILE_SIZE))
    image.blit(tileSpr.spr[32], (25 * TILE_SIZE, 2 * TILE_SIZE))
    image.blit(tileSpr.spr[33], (24 * TILE_SIZE, 3 * TILE_SIZE))
    image.blit(tileSpr.spr[34], (25 * TILE_SIZE, 3 * TILE_SIZE))
    image.set_colorkey((0, 0, 0))

    return image

# 애니메이션 행동 변경 함수
def change_playerAction(frame, action_var, new_var, frameSpd, new_frameSpd, aniMode, new_aniMode):
    if action_var != new_var:
        action_var = new_var
        frame = 0
        frameSpd = new_frameSpd
        aniMode = new_aniMode

    return frame, action_var, frameSpd, aniMode