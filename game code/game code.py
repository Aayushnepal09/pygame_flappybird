import pygame  # importing pygame
import sys  # importing sys
import random  # importing random

# initialize pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((500, 700))
# title and icon
pygame.display.set_caption("FLAPPYBIRD")
icon = pygame.image.load('redbird-downflap.png')
pygame.display.set_icon(icon)

# Adjusting game speed
clock = pygame.time.Clock()

# adding background image
bg_surface = pygame.image.load('background-day.png')
bg_surface = pygame.transform.scale(bg_surface, (500, 700))

# adding floor image
floor_surface = pygame.image.load('base.png')
floor_surface = pygame.transform.scale2x(floor_surface)
floorX = 0

# adding bird
bird = pygame.image.load('redbird-downflap.png')
bird = pygame.transform.scale2x(bird)
bird_box = bird.get_rect(center=(100, 250))
fall = 0.5  # gravity
bird_movement = 0

# adding pipes/multiple pipes
pipe_surface = pygame.image.load('pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [500, 300, 400]


# function to make floor continuously moving in the screen
def floor_movement():
    screen.blit(floor_surface, (floorX, 600))
    screen.blit(floor_surface, (floorX + 500, 600))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 200))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=700:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)


# game loop
while True:

    pygame.display.update()
    clock.tick(150)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if key is Spacebar bird will move upward
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 10
        # adding pipe appear timer
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))

    # bird movement
    screen.blit(bird, bird_box)
    bird_movement += fall
    bird_box.centery += bird_movement

    # pipe movement
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)
    # floor movement
    floorX -= 1
    floor_movement()
    if floorX <= -500:
        floorX = 0
