import sys
import time
import pygame
from random import randint

pygame.init()

# Constants
WIDTH = 1500
HEIGHT = 900
GAME_SPEED = 10
SNAKE_CHUCK = 10
SNAKE_GAP = 3
SNAKE_SIZE = 20
SNAKE_COLOR = "green"

# Initialization
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Snake Game")
fps = pygame.time.Clock()

# Globals
direction = "right"
change_to = direction
current_level = 0
current_question = ""
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
food_positions = []


def change_snake_direction():
    """Changes snake direction based on user input."""
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
    """Modifies snake position based on its direction."""
    if direction == 'up':
        snake_position[1] -= SNAKE_CHUCK
    elif direction == 'down':
        snake_position[1] += SNAKE_CHUCK
    elif direction == 'left':
        snake_position[0] -= SNAKE_CHUCK
    elif direction == 'right':
        snake_position[0] += SNAKE_CHUCK


def draw_snake():
    """Draws the snake on the screen."""
    # add snake length
    grow_snake()

    # remove snake last
    snake_body.pop()

    for index, pos in enumerate(snake_body):
        if index == 0:
            pygame.draw.circle(screen, "red", (pos[0] * SNAKE_GAP + SNAKE_SIZE // 2,
                                               pos[1] * SNAKE_GAP + SNAKE_SIZE // 2), SNAKE_SIZE // 2)
        else:
            pygame.draw.rect(screen, SNAKE_COLOR,
                             pygame.Rect(pos[0] * SNAKE_GAP, pos[1] * SNAKE_GAP, SNAKE_SIZE, SNAKE_SIZE))


def grow_snake():
    """Increases the length of the snake by adding a new segment at the head."""
    snake_body.insert(0, list(snake_position))


def draw_question():
    """Draws the current math question in a box with rounded corners and a calculator icon on the screen."""
    box_width = WIDTH // 6
    box_height = 70
    box_margin = 20
    border_radius = 15

    box_rect = pygame.Rect(box_margin, box_margin, box_width, box_height)
    pygame.draw.rect(screen, "darkgrey", box_rect, border_radius=border_radius)

    # Load the calculator icon
    calculator_icon = pygame.image.load("assets/calculator.svg")
    calculator_icon = pygame.transform.scale(
        calculator_icon, (40, 40))  # Adjust the size as needed

    # Position the calculator icon
    icon_rect = calculator_icon.get_rect(
        topleft=(box_margin + 10, box_margin + 15))
    screen.blit(calculator_icon, icon_rect)

    question_text = pygame.font.SysFont(
        "roboto Mono", 50).render(current_question, True, "white")
    question_text_rect = question_text.get_rect(
        topleft=(icon_rect.right + 10, box_margin + 18))   # Adjust vertical position

    screen.blit(question_text, question_text_rect)


def draw_food():
    """Draws the food items on the screen."""
    for food in food_positions:
        answer_object = pygame.draw.rect(
            screen, "purple", pygame.Rect(food[0], food[1], 30, 30))
        answer_text = pygame.font.SysFont(
            "times new roman", 20).render(f"{food[2]}", True, "black")
        answer_text_object = answer_text.get_rect(center=answer_object.center)
        screen.blit(answer_text, answer_text_object)


def game_over():
    """Displays the game over screen and exits the game."""
    font = pygame.font.SysFont('times new roman', 50)
    game_over_screen = font.render("GAME OVER", True, "red")
    game_over_rect = game_over_screen.get_rect(
        midtop=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.flip()
    time.sleep(3)
    exit_game()


def boundary_check():
    """Checks if the snake has hit the game boundaries."""
    if snake_position[0] < 0 or snake_position[0] * SNAKE_GAP > WIDTH - 10 or \
            snake_position[1] < 0 or snake_position[1] * SNAKE_GAP > HEIGHT - 10:
        game_over()


def snake_body_check():
    """Checks if the snake has collided with itself."""
    for block in snake_body[1:]:
        if snake_position[0] + SNAKE_GAP == block[0] + SNAKE_GAP and snake_position[1] + SNAKE_GAP == block[1] + SNAKE_GAP:
            game_over()


def game_logic():
    """Handles the main game logic, including collisions and level updates."""
    change_snake_direction()
    modify_snake_pos()
    boundary_check()
    snake_body_check()
    spawn_food()


def spawn_food():
    """Spawns food items on the screen based on the current level."""
    global current_level
    seconds = pygame.time.get_ticks() // 1000
    if seconds % GAME_SPEED == 0 and seconds != current_level:
        grow_snake()
        food_positions.clear()
        num1, num2 = randint(1, 10), randint(1, 10)
        global current_question
        current_question = f"{num1} + {num2}"
        food_positions.append(
            [randint(10, WIDTH - 10), randint(10, HEIGHT - 10), num1 + num2])
        for _ in range(3):
            food_positions.append(
                [randint(10, WIDTH - 10), randint(10, HEIGHT - 10), randint(0, 50)])
        current_level = seconds


def reset():
    global change_to
    global direction
    global snake_position
    global snake_body
    global current_level
    global current_question
    global food_positions

    direction = "right"
    change_to = direction
    current_level = 0
    current_question = ""
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    food_positions = []


def exit_game():
    """Exits the game."""
    pygame.quit()
    sys.exit()


def main():
    global change_to
    global direction
    global snake_position
    global snake_body
    global current_level
    global current_question

    # reset for new game
    reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    change_to = 'up'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    change_to = 'down'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    change_to = 'left'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    change_to = 'right'

        # load game logic
        game_logic()

        # set background
        screen.fill("black")

        # show question
        draw_question()

        # show answers
        draw_food()

        # show snake
        draw_snake()

        pygame.display.update()

        fps.tick(GAME_SPEED)


if __name__ == "__main__":
    main()
