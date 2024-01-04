import pygame

pygame.init()

WIDTH = 1500
HEIGHT = 900
GAME_SPEED = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Snake Game")

fps = pygame.time.Clock()


def main():
    running = True

    snake_position = [100, 50]

    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]
    direction = "right"
    change_to = direction
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'up'
                if event.key == pygame.K_DOWN:
                    change_to = 'down'
                if event.key == pygame.K_LEFT:
                    change_to = 'left'
                if event.key == pygame.K_RIGHT:
                    change_to = 'right'

        if change_to == 'up' and direction != 'down':
            direction = 'up'
        if change_to == 'down' and direction != 'up':
            direction = 'down'
        if change_to == 'left' and direction != 'right':
            direction = 'left'
        if change_to == 'right' and direction != 'left':
            direction = 'right'

        if direction == 'up':
            snake_position[1] -= 10
        if direction == 'down':
            snake_position[1] += 10
        if direction == 'left':
            snake_position[0] -= 10
        if direction == 'right':
            snake_position[0] += 10

        screen.fill("black")

        snake_body.insert(0, list(snake_position))

        snake_body.pop()

        for pos in snake_body:
            pygame.draw.rect(screen, "green",
                             pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.display.update()
        fps.tick(GAME_SPEED)


if __name__ == "__main__":
    main()
