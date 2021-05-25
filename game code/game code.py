import pygame  # importing pygame
import sys  # importing sys

# initialize pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((500, 500))

# title and icon
pygame.display.set_caption("FLAPPY BIRD")
icon = pygame.image.load('redbird-upflap.png')
pygame.display.set_icon(icon)

# Adjusting game speed
speed = pygame.time.Clock()

# adding background image
background = pygame.image.load('background-day.png')
background = pygame.transform.scale(background, (500, 500))

# adding floor image
floor = pygame.image.load('base.png')
floor = pygame.transform.scale2x(floor)
floorX = 0

# adding bird
bird = pygame.image.load('bluebird-midflap.png')
bird = pygame.transform.scale2x(bird)
bird_box = bird.get_rect(center=(100, 250))
fall = 0.5  # gravity
bird_movement = 0

# adding pipes/multipal pipes
pipe_load = pygame.image.load('pipe-green.png')
pipe_load = pygame.transform.scale2x(pipe_load)
pipe_list = []
pipe_timer = pygame.USEREVENT
pygame.time.set_timer(pipe_timer, 1000)


# function to make floor continuously moving in the screen
def floor_movement():
    screen.blit(floor, (floorX, 400))
    screen.blit(floor, (floorX + 500, 400))


def pipe_appear():
    pipe_new = pipe_load.get_rect(midtop=(200, 250))
    return pipe_new


def pipe_movement(pipes):
    for pipe in pipes:
        pipe.center -= 5
        return pipes


# game loop
while True:

    pygame.display.update()
    speed.tick(150)

    for movement in pygame.event.get():
        if movement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if key is Spacebar bird will move upward
        if movement.type == pygame.KEYDOWN:
            if movement.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 10
        if movement.type == pipe_timer:
            pipe_list.append(pipe_appear())
    screen.blit(background, (0, 0))

    # bird movement
    screen.blit(bird, bird_box)
    bird_movement += fall
    bird_box.centery += bird_movement

    # floor movement
    floorX -= 1
    floor_movement()
    if floorX <= -500:
        floorX = 0
