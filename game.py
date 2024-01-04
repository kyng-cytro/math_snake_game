import os
import pygame

pygame.init()

WIDTH = 1500
HEIGHT = 900
GAME_SPEED = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Snake Game")

fps = pygame.time.Clock()

bg = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background.jpg')), (WIDTH, HEIGHT))


def change_snake_direction(change_to, direction):
    if change_to == 'up' and direction != 'down':
        return 'up'
    if change_to == 'down' and direction != 'up':
        return 'down'
    if change_to == 'left' and direction != 'right':
        return 'left'
    if change_to == 'right' and direction != 'left':
        return 'right'

    return direction


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

        direction = change_snake_direction(change_to, direction)

        if direction == 'up':
            snake_position[1] -= 10
        if direction == 'down':
            snake_position[1] += 10
        if direction == 'left':
            snake_position[0] -= 10
        if direction == 'right':
            snake_position[0] += 10

        screen.blit(bg, (0, 0))

        snake_body.insert(0, list(snake_position))

        snake_body.pop()

        for pos in snake_body:
            pygame.draw.rect(screen, "green",
                             pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.display.update()
        fps.tick(GAME_SPEED)


if __name__ == "__main__":
    main()
