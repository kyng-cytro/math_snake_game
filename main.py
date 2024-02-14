import sys
import pygame
from button import Button
from random import randint, choice

pygame.init()
pygame.mixer.init()

# Constants
NAME = "Snake Game"
WIDTH = 1280
HEIGHT = 720
GAME_SPEED = 7
SNAKE_CHUCK = 10
SNAKE_GAP = 3
SNAKE_SIZE = 20
FOOD_BACKGROUND_COLOR = "#b68f40"
FOOD_TEXT_COLOR = "white"
CARD_BACKGROUND_COLOR = "#b68f40"
CARD_TEXT_COLOR = "white"
SNAKE_HEAD_COLOR = "#b68f40"
SNAKE_BODY_COLOR = "#d7fcd4"
BG = pygame.image.load("assets/Background.png")


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
    calculator_icon = pygame.image.load("assets/Calculator.svg")
    calculator_icon = pygame.transform.scale(
        calculator_icon, (40, 40))

    # Position the calculator icon
    icon_rect = calculator_icon.get_rect(
        topleft=(box_margin + 10, box_margin + 15))
    screen.blit(calculator_icon, icon_rect)

    question_text = get_font(25).render(
        current_question['question'].upper(), True, CARD_TEXT_COLOR)
    question_text_rect = question_text.get_rect(
        topleft=(icon_rect.right + 10, box_margin + 24))
    screen.blit(question_text, question_text_rect)


def draw_score():
    """Draws the current math question in a box with rounded corners and a calculator icon on the screen."""
    global score
    box_width = WIDTH // 8
    box_height = 70
    box_margin = 20
    border_radius = 15

    box_rect = pygame.Rect(WIDTH - box_width - box_margin,
                           box_margin, box_width, box_height)
    pygame.draw.rect(screen, CARD_BACKGROUND_COLOR,
                     box_rect, border_radius=border_radius)

    # Load the goal icon
    goal_icon = pygame.image.load("assets/Goal.svg")
    goal_icon = pygame.transform.scale(
        goal_icon, (40, 40))

    # Position the goal icon
    icon_rect = goal_icon.get_rect(
        topleft=(box_rect.x + 10, box_rect.y + 15))
    screen.blit(goal_icon, icon_rect)

    score_text = get_font(25).render(f"{score}", True, CARD_TEXT_COLOR)
    score_text_rect = score_text.get_rect(
        topleft=(icon_rect.right + 10, box_rect.y + 24))

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
                pygame.mixer.music.load("assets/Correct.mp3")
                pygame.mixer.music.play()
            else:
                grow_snake()
                pygame.mixer.music.load("assets/Wrong.mp3")
                pygame.mixer.music.play()

            food_positions.clear()
            break


# Helpers
def init_game_logic():
    change_snake_direction()
    modify_snake_pos()
    boundary_check()
    snake_body_check()
    food_check()
    draw_question()
    draw_score()
    draw_food()
    draw_snake()


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


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
    operator = choice(['+', '-', 'x', '÷'])

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


def reset():
    """
    Resets the game state to the initial values.
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


def play():
    """Starts the game"""
    global change_to
    global direction
    global snake_position
    global snake_body
    global current_level
    global current_question
    global instructions

    # reset for new game
    reset()

    # start timer
    pygame.time.set_timer(food_event, 10000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == food_event:
                spawn_food()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    change_to = 'up'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    change_to = 'down'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    change_to = 'left'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    change_to = 'right'

        screen.blit(BG, (0, 0))

        init_game_logic()

        pygame.display.update()

        fps.tick(GAME_SPEED)


def help():
    """Shows help message"""
    while True:
        HELP_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        HELP_TEXT = get_font(45).render(
            "Eat right answers,", True, "black")
        HELP_RECT = HELP_TEXT.get_rect(center=(640, 260))
        screen.blit(HELP_TEXT, HELP_RECT)

        HELP_TEXT1 = get_font(45).render(
            "avoid walls.", True, "black")
        HELP_RECT1 = HELP_TEXT1.get_rect(center=(640, 320))
        screen.blit(HELP_TEXT1, HELP_RECT1)

        HELP_TEXT2 = get_font(45).render(
            "Improve math skills!", True, "black")
        HELP_RECT2 = HELP_TEXT2.get_rect(center=(640, 380))
        screen.blit(HELP_TEXT2, HELP_RECT2)

        HELP_BACK = Button(image=None, pos=(640, 550),
                           text_input="BACK", font=get_font(75), base_color="black", hovering_color="Green")

        HELP_BACK.changeColor(HELP_MOUSE_POS)
        HELP_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HELP_BACK.checkForInput(HELP_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def game_over():
    pygame.mixer.music.load("assets/GameOver.mp3")
    pygame.mixer.music.play()
    main_menu()


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render(NAME.upper(), True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/PlayRect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HELP_BUTTON = Button(image=pygame.image.load("assets/PlayRect.png"), pos=(640, 400),
                             text_input="HELP", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/QuitRect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, HELP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    help()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
