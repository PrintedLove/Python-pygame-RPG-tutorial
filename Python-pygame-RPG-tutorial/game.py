# [Python pygame Game] RPG tutorial
# Made by "PrintedLove"
# Referred to DaFluffyPotato's 'Physics - Pygame Tutorial: Making a Platformer'
#-*-coding: utf-8

import pygame, sys
from datafile import *
from pygame.locals import *
pygame.init()

#게임 컨트롤 변수
pygame.display.set_caption('RPG tutorial')                                      # 창 이름 설정
clock = pygame.time.Clock()

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
screen_scaled = pygame.Surface((WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 4))        # 확대한 스크린

# 리소스 불러오기
spr_player = SpriteSheet('spriteSheet1.png', 16, 16, 8, 8, 11)
spr_map1 = SpriteSheet('spriteSheet3.png', 8, 8, 16, 16, 87)

mapImage = createMapImage(spr_map1)

# 플레이어 컨트롤 변수
keyLeft = False
keyRight = False

player_rect = pygame.Rect((64, 20), (6, 14))
player_movement = [0, 0]            # 플레이어 프레임당 속도
player_vspeed = 0                   # 플레이어 y가속도
player_flytime = 0

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
    collision_types = {'top' : False, 'bottom' : False, 'right' : False, 'left' : False}
    rect.x += movement[0]
    hit_list = collision_floor(rect)

    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_floor(rect)

    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types

# 메인 루프
while True:
    screen_scaled.fill((27, 25, 25))            # 화면 초기화

    screen_scaled.blit(mapImage, (0, 0))        # 맵 드로우

    # 플레이어 컨트롤
    player_movement = [0, 0]
    if keyLeft:
        player_movement[0] -= 1
    if keyRight:
        player_movement[0] += 1
    player_movement[1] += player_vspeed

    player_vspeed += 0.2
    if player_vspeed > 3:
        player_vspeed = 3

    player_rect, player_collision = move(player_rect, player_movement)       # 플레이어 이동

    if player_collision['bottom']:
        player_vspeed = 0
        player_flytime = 0
    else:
        player_flytime += 1

    screen_scaled.blit(spr_player.spr[0], (player_rect.x - 5, player_rect.y - 2))      # 플레이어 드로우

    # 이벤트 컨트롤
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                keyLeft = True
            if event.key == K_RIGHT:
                keyRight = True
            if event.key == K_UP and player_flytime < 6:
                player_vspeed = -3
        if event.type == KEYUP:
            if event.key == K_LEFT:
                keyLeft = False
            if event.key == K_RIGHT:
                keyRight = False

    surf = pygame.transform.scale(screen_scaled, WINDOW_SIZE)       # 창 배율 적용
    screen.blit(surf, (0, 0))

    pygame.display.update()
    clock.tick(60)