# Import necessary modules
import random
import sys
import pygame
from pygame.locals import *

# Game Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 499
ELEVATION = WINDOW_HEIGHT * 0.8
FRAME_PER_SECOND = 32

# Asset file paths
PIPE_IMAGE_PATH = 'images/pipe.png'
BACKGROUND_IMAGE_PATH = 'images/background.jpg'
BIRD_IMAGE_PATH = 'images/bird.png'
SEA_LEVEL_IMAGE_PATH = 'images/base.jfif'

# Initialize Pygame and create window
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird Game')
frame_per_second_clock = pygame.time.Clock()

# Load game images
game_images = {
    'score_images': [pygame.image.load(f'images/{i}.png').convert_alpha() for i in range(10)],
    'bird': pygame.image.load(BIRD_IMAGE_PATH).convert_alpha(),
    'sea_level': pygame.image.load(SEA_LEVEL_IMAGE_PATH).convert_alpha(),
    'background': pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha(),
    'pipe': (
        pygame.transform.rotate(pygame.image.load(PIPE_IMAGE_PATH).convert_alpha(), 180),
        pygame.image.load(PIPE_IMAGE_PATH).convert_alpha()
    )
}

def main():
    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")
    while True:
        horizontal = int(WINDOW_WIDTH / 5)
        vertical = int((WINDOW_HEIGHT - game_images['bird'].get_height()) / 2)
        ground = 0
        display_start_screen(horizontal, vertical, ground)
        flappy_game()

def display_start_screen(horizontal, vertical, ground):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                window.blit(game_images['background'], (0, 0))
                window.blit(game_images['bird'], (horizontal, vertical))
                window.blit(game_images['sea_level'], (ground, ELEVATION))
                pygame.display.update()
                frame_per_second_clock.tick(FRAME_PER_SECOND)

def flappy_game():
    your_score = 0
    horizontal = int(WINDOW_WIDTH / 5)
    vertical = int(WINDOW_WIDTH / 2)
    ground = 0
    mytempheight = 100

    first_pipe = create_pipe()
    second_pipe = create_pipe()

    down_pipes = [
        {'x': WINDOW_WIDTH + 300 - mytempheight, 'y': first_pipe[1]['y']},
        {'x': WINDOW_WIDTH + 300 - mytempheight + (WINDOW_WIDTH / 2), 'y': second_pipe[1]['y']}
    ]
    up_pipes = [
        {'x': WINDOW_WIDTH + 300 - mytempheight, 'y': first_pipe[0]['y']},
        {'x': WINDOW_WIDTH + 200 - mytempheight + (WINDOW_WIDTH / 2), 'y': second_pipe[0]['y']}
    ]

    pipe_velocity_x = -4
    bird_velocity_y = -9
    bird_max_velocity_y = 10
    bird_min_velocity_y = -8
    bird_acceleration_y = 1
    bird_flap_velocity = -8
    bird_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        if is_game_over(horizontal, vertical, up_pipes, down_pipes):
            return

        player_mid_pos = horizontal + game_images['bird'].get_width() / 2
        for pipe in up_pipes:
            pipe_mid_pos = pipe['x'] + game_images['pipe'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                your_score += 1
                print(f"Your score is {your_score}")

        if bird_velocity_y < bird_max_velocity_y and not bird_flapped:
            bird_velocity_y += bird_acceleration_y

        if bird_flapped:
            bird_flapped = False

        player_height = game_images['bird'].get_height()
        vertical = vertical + min(bird_velocity_y, ELEVATION - vertical - player_height)

        for upper_pipe, lower_pipe in zip(up_pipes, down_pipes):
            upper_pipe['x'] += pipe_velocity_x
            lower_pipe['x'] += pipe_velocity_x

        if 0 < up_pipes[0]['x'] < 5:
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])

        if up_pipes[0]['x'] < -game_images['pipe'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        window.blit(game_images['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            window.blit(game_images['pipe'][1], (lower_pipe['x'], lower_pipe['y']))

        window.blit(game_images['sea_level'], (ground, ELEVATION))
        window.blit(game_images['bird'], (horizontal, vertical))

        display_score(your_score)

        pygame.display.update()
        frame_per_second_clock.tick(FRAME_PER_SECOND)

def is_game_over(horizontal, vertical, up_pipes, down_pipes):
    if vertical > ELEVATION - 25 or vertical < 0:
        return True

    for pipe in up_pipes:
        pipe_height = game_images['pipe'][0].get_height()
        if vertical < pipe_height + pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipe'][0].get_width():
            return True

    for pipe in down_pipes:
        if (vertical + game_images['bird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipe'][0].get_width():
            return True

    return False

def create_pipe():
    offset = WINDOW_HEIGHT / 3
    pipe_height = game_images['pipe'][0].get_height()
    y2 = offset + random.randrange(0, int(WINDOW_HEIGHT - game_images['sea_level'].get_height() - 1.2 * offset))
    pipe_x = WINDOW_WIDTH + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},
        {'x': pipe_x, 'y': y2}
    ]
    return pipe

def display_score(score):
    numbers = [int(x) for x in list(str(score))]
    width = sum(game_images['score_images'][num].get_width() for num in numbers)
    x_offset = (WINDOW_WIDTH - width) / 1.1
    for num in numbers:
        window.blit(game_images['score_images'][num], (x_offset, WINDOW_WIDTH * 0.02))
        x_offset += game_images['score_images'][num].get_width()

if __name__ == "__main__":
    main()
