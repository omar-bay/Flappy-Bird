import pygame
import sys
import random

def game_floor():
    screen.blit(floor_base, (floor_x_pos, 900))
    screen.blit(floor_base, (floor_x_pos+576, 900))

def check_collision(pipes):
    # hit pipe
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    # check floor not hit
    if bird_rect.top <= -100 or bird_rect.bottom >=900:
        print('hit head')
        return False
    return True

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos-300))
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5

    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

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

message = pygame.image.load("flappy-bird-assets/sprites/message.png").convert_alpha()
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center=(288, 512))

# building pipes
pipe_surface = pygame.image.load("flappy-bird-assets/sprites/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400, 600, 800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)


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
                pipe_list.clear()
                game_active = True
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    screen.blit(background, (0, 0))

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)

        # draw pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # check for collision
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect)

    # create floor
    floor_x_pos -= 1
    game_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)