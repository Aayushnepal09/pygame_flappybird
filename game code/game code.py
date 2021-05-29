import pygame  # importing pygame
import sys  # importing sys

# initialize pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((500,500))
# title and icon
pygame.display.set_caption("FLAPPYBIRD")
icon = pygame.image.load('redbird-downflap.png')
pygame.display.set_icon(icon)

# Adjusting game speed
clock = pygame.time.Clock()

# adding background image
bg_surface = pygame.image.load('background-day.png')
bg_surface = pygame.transform.scale(bg_surface, (500, 500))

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
pipe_load = pygame.image.load('pipe-green.png')
pipe_load = pygame.transform.scale2x(pipe_load)
pipe_list = []
pipe_timer = pygame.USEREVENT
pygame.time.set_timer(pipe_timer, 1000)


# function to make floor continuously moving in the screen
def floor_movement():
    screen.blit(floor_surface, (floorX, 400))
    screen.blit(floor_surface, (floorX + 500, 400))


def pipe_appear():
    pipe_new = pipe_load.get_rect(midtop=(200, 250))
    return pipe_new


def pipe_movement(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe_timer in pipes:
        screen.blits(pipe_load,pipe_timer)



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
        if event.type == pipe_timer:
            pipe_list.append(pipe_appear())
    screen.blit(bg_surface, (0, 0))

    # bird movement
    screen.blit(bird, bird_box)
    bird_movement += fall
    bird_box.centery += bird_movement
    #pipe movement
    pipe_list=pipe_movement(pipe_list)
    draw_pipes(pipe_list)
    # floor movement
    floorX -= 1
    floor_movement()
    if floorX <= -500:
        floorX = 0
