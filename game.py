import pygame

pygame.init()

# constants
WIDTH = 1500
HEIGHT = 900
GAME_SPEED = 15
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
              [60, 50],
              [50, 50]
              ]


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


def main():
    global change_to
    global direction
    global snake_position
    global snake_body

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

        # add snake length
        snake_body.insert(0, list(snake_position))

        # remove snake length
        snake_body.pop()

        for pos in snake_body:
            pygame.draw.rect(screen, SNAKE_COLOR,
                             pygame.Rect(pos[0] * SNAKE_GAP, pos[1] * SNAKE_GAP, SNAKE_SIZE, SNAKE_SIZE))

        pygame.display.update()
        fps.tick(GAME_SPEED)


if __name__ == "__main__":
    main()
