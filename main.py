import pygame
import sys
import random

def game_floor():
    screen.blit(floor_base, (floor_x_pos, 900))
    screen.blit(floor_base, (floor_x_pos+576, 900))

def check_collision():
    # check floor not hit
    if bird_rect.top <= -100 or bird_rect.bottom >=900:
        print('hit head')
        return False
    return True

pygame.init()

# vars
game_active = True
gravity = 0.25
bird_movement = 0

clock = pygame.time.Clock()

screen = pygame.display.set_mode((576, 1024))

background = pygame.image.load("flappy-bird-assets/sprites/background-day.png").convert()
background = pygame.transform.scale2x(background)

bird = pygame.image.load("flappy-bird-assets/sprites/bluebird-midflap.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 512))

floor_base = pygame.image.load("flappy-bird-assets/sprites/base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_pos = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
            if event.key == pygame.K_SPACE and not game_active:
                bird.rect.center = (100, 512)
                bird_movement = 0
                game_active = True

    screen.blit(background, (0, 0))

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)

        # check for collision
        game_active = check_collision()
    else:
        print('game over')

    # create floor
    floor_x_pos -= 1
    game_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)