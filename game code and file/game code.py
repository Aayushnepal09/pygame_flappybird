import pygame  # importing pygame
import sys  # importing sys
import random  # importing random

# initialize pygame
pygame.init()

game_font = pygame.font.Font('flappy bird.ttf', 50)

# creating a screen

screen = pygame.display.set_mode((500, 700))

# title and icon
pygame.display.set_caption("FLAPPY BIRD")
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


# function to make floor continuously moving in the screen
def floor_movement():
    screen.blit(floor_surface, (floorX, 600))
    screen.blit(floor_surface, (floorX + 500, 600))


# adding bird
bird_surface = pygame.image.load('redbird-downflap.png')
bird_surface = pygame.transform.scale2x(bird_surface)
bird_box = bird_surface.get_rect(center=(100, 250))
fall = 0.5  # gravity
bird_movement = 0


# function to make bird rotate by little while flying
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 5, 1)
    return new_bird


# adding pipes/multiple pipes
pipe_surface = pygame.image.load('pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
#creating a pipe list
pipe_list = []

#adding timer gor the pipes to appare and reappare
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

#adding diffrent pipe hieght
pipe_height = [500, 300, 400]

#functions to adjust pipe height
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 200))
    return bottom_pipe, top_pipe

#function to make diffrent pipe spawn on the screen
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


#function to make pipe moveleft by a bit
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


# adding sound
bird_sound = pygame.mixer.Sound('flap.wav')
collision_sound = pygame.mixer.Sound('co.wav')
score_sound = pygame.mixer.Sound('passing pol.wav')
score_sound_countdown = 100
background_sound = pygame.mixer.Sound('background.mp3')

# variables for collision
game_active = True
def check_collission(pipes):
    for pipe in pipes:
        if bird_box.colliderect(pipe):
            collision_sound.play()
            return False

    if bird_box.top <= 0 or bird_box.bottom >= 604:
        collision_sound.play()
        return False

    return True

# variables for score

score = 0

# high score is stored in a different file
with open("HighScore.txt", "r") as file:
    high_score = int(file.read())
    file.close()


#function to display the score
def score_display(game_state):
    #displaying only current score while game is running
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (200, 0, 200))
        score_rect = score_surface.get_rect(center=(250, 30))
        screen.blit(score_surface, score_rect)

    #displaying both current and highscore in game over screen
    if game_state == 'Game over':
        score_surface = game_font.render(f'current score: {(int(score))}', True, (200, 0, 200))
        score_rect = score_surface.get_rect(center=(250, 30))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'high score: {(int(high_score))}' ' ' 'Press space bar to restart', True,
                                              (200, 0, 200))
        high_score_rect = high_score_surface.get_rect(center=(250, 70))
        screen.blit(high_score_surface, high_score_rect)

#functun to check if the score is greater than current highscore and updating high score file
def update_score(score, high_score):
    if score > high_score:
        high_score = score
        high_score = int(high_score)
        with open("HighScore.txt", "w") as file:
            file.write(str(high_score))
    return high_score

# adding game over screen
game_over_surface = pygame.image.load('game_over_PNG59.png')
game_over_rect = game_over_surface.get_rect(center=(250, 350))



# game loop
while True:

    pygame.display.update()
    clock.tick(150)
    # background_sound.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if key is Spacebar bird will move upward
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 10
                bird_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_box.center = (100, 250)
                bird_movement = 0
                score = 0

        # adding pipe appear timer
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))
    if game_active:
        # bird movement

        bird_movement += fall
        rotated_bird = rotate_bird(bird_surface)
        bird_box.centery += bird_movement
        screen.blit(rotated_bird, bird_box)

        game_active = check_collission(pipe_list)

        # pipe movement
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        # score  display
        score += 0.0109

        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown == 0:
            score_sound.play()
            score_sound_countdown = 100


    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('Game over')

    # floor movement
    floorX -= 1
    floor_movement()
    if floorX <= -500:
        floorX = 0
