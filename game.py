import sys
import time
import pygame
from random import randint, choice

pygame.init()

# Constants
NAME = "Snake Game"
WIDTH = 1500
HEIGHT = 900
GAME_SPEED = 10
SNAKE_CHUCK = 10
SNAKE_GAP = 3
SNAKE_SIZE = 20
FOOD_BACKGROUND_COLOR = "lightgray"
FOOD_TEXT_COLOR = "black"
CARD_BACKGROUND_COLOR = "darkgrey"
CARD_TEXT_COLOR = "white"
BACKDROP_COLOR = "black"
SNAKE_HEAD_COLOR = "red"
SNAKE_BODY_COLOR = "green"


# Initialization
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(NAME)
fps = pygame.time.Clock()

# Globals
instructions = True
direction = "right"
change_to = direction
score = 0
current_question = {"question": "", "answer": 0}
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
food_positions = []
food_event = pygame.USEREVENT + 0


# Draws
def draw_snake():
    """Draws the snake on the screen."""
    # add snake length
    grow_snake()

    # remove snake last
    snake_body.pop()

    for index, pos in enumerate(snake_body):
        x = pos[0] * SNAKE_GAP
        y = pos[1] * SNAKE_GAP
        pygame.draw.rect(screen, SNAKE_HEAD_COLOR if index == 0 else SNAKE_BODY_COLOR,
                         position_to_rect(x, y, SNAKE_SIZE), border_radius=20 if index == 0 else 0)


def draw_question():
    """Draws the current math question in a box with rounded corners and a calculator icon on the screen."""
    box_width = WIDTH // 6
    box_height = 70
    box_margin = 20
    border_radius = 15

    box_rect = pygame.Rect(box_margin, box_margin, box_width, box_height)
    pygame.draw.rect(screen, CARD_BACKGROUND_COLOR,
                     box_rect, border_radius=border_radius)

    # Load the calculator icon
    calculator_icon = pygame.image.load("assets/calculator.svg")
    calculator_icon = pygame.transform.scale(
        calculator_icon, (40, 40))

    # Position the calculator icon
    icon_rect = calculator_icon.get_rect(
        topleft=(box_margin + 10, box_margin + 15))
    screen.blit(calculator_icon, icon_rect)

    question_text = pygame.font.SysFont(
        "roboto Mono", 50).render(current_question["question"], True, CARD_TEXT_COLOR)
    question_text_rect = question_text.get_rect(
        topleft=(icon_rect.right + 10, box_margin + 18))
    screen.blit(question_text, question_text_rect)


def draw_score():
    """Draws the current math question in a box with rounded corners and a calculator icon on the screen."""
    global score
    box_width = WIDTH // 10
    box_height = 70
    box_margin = 20
    border_radius = 15

    box_rect = pygame.Rect(WIDTH - box_width - box_margin,
                           box_margin, box_width, box_height)
    pygame.draw.rect(screen, CARD_BACKGROUND_COLOR,
                     box_rect, border_radius=border_radius)

    # Load the goal icon
    goal_icon = pygame.image.load("assets/goal.svg")
    goal_icon = pygame.transform.scale(
        goal_icon, (40, 40))

    # Position the goal icon
    icon_rect = goal_icon.get_rect(
        topleft=(box_rect.x + 10, box_rect.y + 15))
    screen.blit(goal_icon, icon_rect)

    score_text = pygame.font.SysFont(
        "roboto Mono", 50).render(f"{score}", True, CARD_TEXT_COLOR)
    score_text_rect = score_text.get_rect(
        topleft=(icon_rect.right + 10, box_rect.y + 18))

    screen.blit(score_text, score_text_rect)


def draw_food():
    """Draws the food items on the screen."""
    for food in food_positions:
        answer_object = pygame.draw.rect(
            screen,  FOOD_BACKGROUND_COLOR, position_to_rect(food[0], food[1], 30), border_radius=20)
        answer_text = pygame.font.SysFont(
            "roboto Mono", 25).render(f"{food[2]}", True, FOOD_TEXT_COLOR)
        answer_text_object = answer_text.get_rect(center=answer_object.center)
        screen.blit(answer_text, answer_text_object)


def draw_instructions():
    font = pygame.font.Font(None, 24)

    # Banner
    banner_text = font.render("Math Snake Game", True, "white")
    banner_rect = banner_text.get_rect(center=(WIDTH // 2, 100))

    # Instructions paragraph
    instructions_lines = [
        "Welcome to Math Snake Game! Eat the numbers by answering the math questions correctly. ",
        "Use arrow keys to navigate. Avoid collisions with the walls and yourself. ",
        "Have fun and improve your math skills!",
    ]

    # Padding for the text boxes
    padding = 20

    # Banner box
    pygame.draw.rect(screen, "gray", banner_rect.inflate(
        50, 50), border_radius=8)
    screen.blit(banner_text, banner_rect)

    # Instructions box
    instructions_surfaces = [font.render(
        line, True, "white") for line in instructions_lines]
    instructions_rects = [surface.get_rect(center=(
        WIDTH // 2, 200 + i * 40)) for i, surface in enumerate(instructions_surfaces)]

    for surface, rect in zip(instructions_surfaces, instructions_rects):
        pygame.draw.rect(screen, "gray", rect.inflate(
            padding, padding), border_radius=8)
        screen.blit(surface, rect)


# Checks
def boundary_check():
    """Checks if the snake has hit the game boundaries."""
    if snake_position[0] < 0 or snake_position[0] * SNAKE_GAP > WIDTH - 10 or \
            snake_position[1] < 0 or snake_position[1] * SNAKE_GAP > HEIGHT - 10:
        game_over()


def snake_body_check():
    """Checks if the snake has collided with itself."""
    for block in snake_body[1:]:
        head = position_to_rect(
            snake_position[0], snake_position[1], SNAKE_SIZE, SNAKE_GAP)
        body = position_to_rect(block[0], block[1], SNAKE_SIZE, SNAKE_GAP)
        if head.colliderect(body):
            game_over()


def food_check():
    """Checks if the snake has collided with food items."""
    global score
    global food_positions
    global snake_position
    for food in food_positions:
        food_x, food_y = food[0], food[1]
        snake_x, snake_y = snake_position[0], snake_position[1]
        foodRect = position_to_rect(food_x, food_y, 30)
        snakeRect = position_to_rect(snake_x, snake_y, SNAKE_SIZE, SNAKE_GAP)
        if foodRect.colliderect(snakeRect):
            if (food[2] == current_question['answer']):
                score += 10
            else:
                grow_snake()

            food_positions.clear()
            break


# Helpers
def position_to_rect(x, y, size, gap=1):
    """
    Converts a position (x, y) to a pygame Rect object with the specified size and gap.
    """
    return pygame.Rect(x*gap, y*gap, size, size)


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


def grow_snake():
    """Increases the length of the snake by adding a new segment at the head."""
    snake_body.insert(0, list(snake_position))


def generate_random_position(excluded_positions=[]):
    """Generates a random position on the screen, excluding positions in the excluded_positions list."""
    while True:
        x = randint(10, WIDTH - 30)
        y = randint(70, HEIGHT - 40)
        if [x, y] not in excluded_positions:
            return [x, y]


def generate_random_question():
    """Generates a random arithmetic question."""
    num1 = randint(1, 10)
    num2 = randint(1, 10)
    operator = choice(['+', '-', 'x', '/'])

    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    elif operator == 'x':
        answer = num1 * num2
    else:
        num2 = randint(1, min(10, num1))
        answer = num1 // num2

    return f"{num1} {operator} {num2}", answer


def generate_wrong_options(correct_answer):
    """Generates three unique wrong answer options close to the correct answer, excluding the correct answer."""
    deviation = 4
    wrong_options = set()
    while len(wrong_options) < 3:
        wrong_option = correct_answer
        while wrong_option == correct_answer or wrong_option in wrong_options:
            wrong_option = randint(
                correct_answer - deviation, correct_answer + deviation)
        wrong_options.add(wrong_option)

    return list(wrong_options)


def spawn_food():
    """Spawns food items on the screen based on the current level."""
    global current_question
    grow_snake()
    food_positions.clear()
    current_question['question'], current_question['answer'] = generate_random_question()
    wrong_options = generate_wrong_options(current_question['answer'])
    food_positions.append(
        [*generate_random_position(
            excluded_positions=food_positions), current_question['answer']])
    for wrong_option in wrong_options:
        food_positions.append(
            [*generate_random_position(excluded_positions=food_positions + snake_body), wrong_option])


def game_over():
    """Displays the game over screen and exits the game."""
    font = pygame.font.SysFont('times new roman', 50)
    game_over_screen = font.render("GAME OVER", True, "red")
    game_over_rect = game_over_screen.get_rect(
        midtop=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.flip()
    pygame.time.set_timer(food_event, 0)
    time.sleep(3)
    main()


def reset():
    """
    Resets the game state to the initial values.

    Global Variables Modified:
    - score: Reset to 0.
    - change_to: Reset to the initial direction ("right").
    - direction: Reset to the initial direction ("right").
    - snake_position: Reset to the initial position [100, 50].
    - snake_body: Reset to the initial body segments.
    - current_level: Not mentioned, assuming it remains unchanged.
    - current_question: Reset to an empty question and answer.
    - food_positions: Cleared to an empty list.
    """
    global score
    global change_to
    global direction
    global snake_position
    global snake_body
    global current_level
    global current_question
    global food_positions

    score = 0
    direction = "right"
    change_to = direction
    current_question = {"question": "", "answer": 0}
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
    global instructions

    # reset for new game
    reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == food_event:
                spawn_food()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (instructions):
                    # start timer
                    pygame.time.set_timer(food_event, 5000)
                    instructions = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    change_to = 'up'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    change_to = 'down'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    change_to = 'left'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    change_to = 'right'

        if instructions:
            screen.fill("black")
            draw_instructions()

        if not instructions:
            screen.fill(BACKDROP_COLOR)

            # switch snake direction
            change_snake_direction()

            # move snake
            modify_snake_pos()

            # check if snake touching edges
            boundary_check()

            # check if snake touching self
            snake_body_check()

            # check if snake touching food
            food_check()

            # show question
            draw_question()

            # show score
            draw_score()

            # show answers
            draw_food()

            # show snake
            draw_snake()

        pygame.display.update()

        fps.tick(GAME_SPEED)


if __name__ == "__main__":
    main()
