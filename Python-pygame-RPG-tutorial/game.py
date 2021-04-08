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

mapImage = createFloorImage(spr_map1)

# 플레이어 컨트롤 변수
player_moveLeft = False
player_moveRight = False

player_position = [50, 50]              # 플레이어 좌표
player_vspeed = 0                       # 플레이어 y가속도

player_rect = pygame.rect.Rect(player_position[0], player_position[1], spr_player.height, spr_player.width)

while True:     # 메인 루프
    screen_scaled.fill((27, 25, 25))            # 화면 초기화

    screen_scaled.blit(mapImage, (0, 0))      # 플레이어 드로우
    screen_scaled.blit(spr_player.spr[10], player_position)      # 플레이어 드로우

    # 플레이어 컨트롤
    if player_position[1] > WINDOW_SIZE[1] / 4 - spr_player.height:
        player_vspeed = -player_vspeed
    else:
        player_vspeed += 0.2
    player_position[1] += player_vspeed

    if player_moveLeft == True:
        player_position[0] -= 4
    if player_moveRight == True:
        player_position[0] += 4

    player_rect.x = player_position[0]
    player_rect.y = player_position[1]

    #if player_rect.colliderect(test_rect):
    #    pygame.draw.rect(screen, (255, 0, 0), test_rect)
    #else:
    #    pygame.draw.rect(screen, (0, 0, 0), test_rect)

    # 이벤트 컨트롤
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player_moveLeft = True
            if event.key == K_RIGHT:
                player_moveRight = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                player_moveLeft = False
            if event.key == K_RIGHT:
                player_moveRight = False

    surf = pygame.transform.scale(screen_scaled, WINDOW_SIZE)       # 창 배율 적용
    screen.blit(surf, (0, 0))

    pygame.display.update()
    clock.tick(60)
