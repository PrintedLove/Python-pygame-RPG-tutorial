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

camera_scroll = [TILE_MAPSIZE[0] * 4, 0]              # 카메라 이동 좌표

# 리소스 불러오기
spriteSheet_player = SpriteSheet('spriteSheet1.png', 16, 16, 8, 8, 12)      # 플레이어 스프라이트 시트
spriteSheet_object = SpriteSheet('spriteSheet2.png', 8, 8, 16, 16, 37)      # 공통 오브젝트 스프라이트 시트
spriteShee_map1 = SpriteSheet('spriteSheet3.png', 8, 8, 16, 16, 87)         # 지형 1 스프라이트 시트

spr_player = {}
spr_player['stay'] = createAnimationSet(spriteSheet_player, [0])
spr_player['run'] = createAnimationSet(spriteSheet_player, 1, 8)            # 플레이어 달리기
spr_player['jump'] = createAnimationSet(spriteSheet_player, [9, 10, 11])        # 플레이어 점프

createMapData()                                 # 맵 데이터 초기화
mapImage = createMapImage(spriteShee_map1)              # 맵 이미지 생성
backImage = createBackImage(spriteSheet_object)         # 배경 이미지 생성


# 플레이어 컨트롤 변수
keyLeft = False
keyRight = False

player_rect = pygame.Rect((TILE_MAPSIZE[0] * 4, TILE_MAPSIZE[1] * 4 - 14), (6, 14))
player_movement = [0, 0]            # 플레이어 프레임당 속도
player_vspeed = 0                   # 플레이어 y가속도
player_flytime = 0                  # 공중에 뜬 시간

player_action = 'stay'              # 플레이어 현재 행동
player_frame = 0                    # 플레이어 애니메이션 프레임
player_frameSpeed = 1               # 플레이어 애니메이션 속도(낮을 수록 빠름. max 1)
player_frameTimer = 0
player_flip = False                 # 플레이어 이미지 반전 여부 (False: RIGHT)
player_animationMode = True         # 애니메이션 모드 (False: 반복, True: 한번)

# 메인 루프
while True:
    screen_scaled.fill(BACKGROUND_COLOR)            # 화면 초기화

    camera_scroll[0] += int((player_rect.x - camera_scroll[0] - WINDOW_SIZE[0] / 8 - 5) / 16)       # 카메라 이동
    camera_scroll[1] += int((player_rect.y - camera_scroll[1] - WINDOW_SIZE[1] / 8 - 2) / 16)

    screen_scaled.blit(backImage, (0, 0))                                   # 배경 드로우
    screen_scaled.blit(mapImage, (-camera_scroll[0], -camera_scroll[1]))    # 맵 드로우

    # 플레이어 컨트롤
    player_movement = [0, 0]                       # 플레이어 이동
    if keyLeft:
        player_movement[0] -= 2
    if keyRight:
        player_movement[0] += 2
    player_movement[1] += player_vspeed

    player_vspeed += 0.2
    if player_vspeed > 3:
        player_vspeed = 3

    if player_movement[0] != 0:                  # 플레이어 걷기 애니메이션 처리 및 방향 전환
        if player_flytime == 0:
            player_frame, player_action, player_frameSpeed, player_animationMode = change_playerAction(
                player_frame, player_action, 'run', player_frameSpeed, 3, player_animationMode, True)

        if player_movement[0] > 0:
            player_flip = False
        else:
            player_flip = True
    else:
        if player_flytime == 0:
            player_frame, player_action, player_frameSpeed, player_animationMode = change_playerAction(
                player_frame, player_action, 'stay', player_frameSpeed, 3, player_animationMode, True)

    player_rect, player_collision = move(player_rect, player_movement)

    if player_collision['bottom']:
        player_vspeed = 0
        player_flytime = 0
    else:
        player_flytime += 1

    player_frameTimer += 1                          # 플레이어 애니메이션 타이머
    if player_frameTimer >= player_frameSpeed:
        player_frame +=1
        player_frameTimer = 0

        if player_frame >= len(spr_player[player_action]):
            if player_animationMode == True:
                player_frame = 0
            else:
                player_frame -= 1

    screen_scaled.blit(pygame.transform.flip(spr_player[player_action][player_frame], player_flip, False)
                       , (player_rect.x - camera_scroll[0] - 5, player_rect.y - camera_scroll[1] - 2))      # 플레이어 드로우

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
                player_vspeed = -3.5
                player_flytime += 1

                player_frame, player_action, player_frameSpeed, player_animationMode = change_playerAction(
                    player_frame, player_action, 'jump', player_frameSpeed, 6, player_animationMode, False)
        if event.type == KEYUP:
            if event.key == K_LEFT:
                keyLeft = False
            if event.key == K_RIGHT:
                keyRight = False

    surf = pygame.transform.scale(screen_scaled, WINDOW_SIZE)       # 창 배율 적용
    screen.blit(surf, (0, 0))

    pygame.display.update()
    clock.tick(60)