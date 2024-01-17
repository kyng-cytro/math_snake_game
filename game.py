import sys
import time
import pygame
from random import randint

pygame.init()

# constants
WIDTH = 1500
HEIGHT = 900
GAME_SPEED = 10
SNAKE_CHUCK = 10
SNAKE_GAP = 3
SNAKE_SIZE = 20
SNAKE_COLOR = "green"

# init
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Snake Game")

fps = pygame.time.Clock()

# globals
direction = "right"
change_to = direction
snake_position = [100, 50]
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50],
              ]

food_positions = []

# changes snakes direction


def change_snake_direction():
    global direction
    global change_to
    if change_to == 'up' and direction != 'down':
        direction = 'up'
    if change_to == 'down' and direction != 'up':
        direction = 'down'
    if change_to == 'left' and direction != 'right':
        direction = 'left'
    if change_to == 'right' and direction != 'left':
        direction = 'right'


def modify_snake_pos():
    if direction == 'up':
        snake_position[1] -= SNAKE_CHUCK
    if direction == 'down':
        snake_position[1] += SNAKE_CHUCK
    if direction == 'left':
        snake_position[0] -= SNAKE_CHUCK
    if direction == 'right':
        snake_position[0] += SNAKE_CHUCK


def boundary_check():
    if snake_position[0] < 0 or snake_position[0] * SNAKE_GAP > WIDTH-10:
        game_over()

    if snake_position[1] < 0 or snake_position[1] * SNAKE_GAP > HEIGHT-10:
        game_over()


def snake_body_check():
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()


def game_over():
    # creating font object my_font
    font = pygame.font.SysFont('times new roman', 50)

    game_over_screen = font.render("GAME OVER", True, "red")

    game_over_rect = game_over_screen.get_rect()

    game_over_rect.midtop = (WIDTH//2, HEIGHT//2)

    screen.blit(game_over_screen, game_over_rect)

    pygame.display.flip()

    time.sleep(3)

    exit_game()


def exit_game():
    pygame.quit()
    sys.exit()


def main():
    global change_to
    global direction
    global snake_position
    global snake_body

    current_level = 0
    current_question = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'up'
                if event.key == pygame.K_DOWN:
                    change_to = 'down'
                if event.key == pygame.K_LEFT:
                    change_to = 'left'
                if event.key == pygame.K_RIGHT:
                    change_to = 'right'

        change_snake_direction()

        modify_snake_pos()

        screen.fill("black")

        seconds = pygame.time.get_ticks() // 1000

        if seconds != 0 and seconds % GAME_SPEED == 0:
            if seconds != current_level:
                # clear
                food_positions.clear()

                num1 = randint(1, 10)
                num2 = randint(1, 10)

                current_question = f"{num1} + {num2}"  # 5  + 5

                # right answer
                food_positions.append(
                    [randint(10, WIDTH-10), randint(10, HEIGHT-10), num1 + num2])  # 10

                # other wrong answers
                for _ in range(3):
                    food_positions.append(
                        [randint(10, WIDTH-10), randint(10, HEIGHT-10), randint(0, 50)])

                current_level = seconds

        # add snake length
        snake_body.insert(0, list(snake_position))

        # remove snake length
        snake_body.pop()

        # TODO: add instruction screen

        boundary_check()

        snake_body_check()

        # Spawn question
        question_text = pygame.font.SysFont(
            "time new roman", 50).render(current_question, True, "white")

        question_text_object = question_text.get_rect(
            center=(WIDTH // 10, HEIGHT // 14))

        screen.blit(question_text, question_text_object)

        # Spawn food
        for food in food_positions:
            answer_object = pygame.draw.rect(screen, "purple",
                                             pygame.Rect(food[0], food[1], 30, 30))
            answer_text = pygame.font.SysFont("times new roman", 20).render(
                f"{food[2]}", True, "black")
            answer_text_object = answer_text.get_rect(
                center=answer_object.center)

            screen.blit(answer_text, answer_text_object)

        # Spawn snake
        for index, pos in enumerate(snake_body):
            if index == 0:
                pygame.draw.circle(
                    screen, "red", (pos[0] * SNAKE_GAP + SNAKE_SIZE // 2, pos[1] * SNAKE_GAP + SNAKE_SIZE // 2), SNAKE_SIZE // 2)
            else:
                pygame.draw.rect(screen, SNAKE_COLOR,
                                 pygame.Rect(pos[0] * SNAKE_GAP, pos[1] * SNAKE_GAP, SNAKE_SIZE, SNAKE_SIZE))

        pygame.display.update()

        # TODO: make game speed faster by score?
        fps.tick(GAME_SPEED)


if __name__ == "__main__":
    main()
