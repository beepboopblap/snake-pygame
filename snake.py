import pygame
from pygame import *
import random
import math
import pickle
import os

def main():

    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500

    pygame.init()
    fps = pygame.time.Clock()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    dir = 0

    Pixel40 = pygame.font.Font("PublicPixel-0W6DP.ttf", 40)
    Pixel20 = pygame.font.Font("PublicPixel-0W6DP.ttf", 20)

    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)

    player_x = 240
    player_y = 220
    apple_x = random.randrange(0,500, 5)
    apple_y = random.randrange(90,490, 5)
    score = 0
    snake_length = 1
    snake_blocks = []
    speed_x = 0
    speed_y = 10
    dir = 0
    game = True
    game_over = False
    game_over_label = Pixel40.render("Game Over", 1, red)


    def isCollision(apple_x, apple_y, player_x, player_y):
        distance = math.sqrt(
            (math.pow(player_x - apple_x, 2)) + (math.pow(player_y - apple_y, 2))
        )
        if distance < 10:
            return True
        else:
            return False

    highScore = pickle.load(open("high_score.txt", "rb"))

    while running:

        if game:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if dir == 2:
                            dir = 2
                        else:
                            dir = 1
                    elif event.key == pygame.K_DOWN:
                        if dir == 1:
                            dir = 1
                        else:
                            dir = 2
                    elif event.key == pygame.K_LEFT:
                        if dir == 4:
                            dir = 4
                        else:
                            dir = 3
                    elif event.key == pygame.K_RIGHT:
                        if dir == 3:
                            dir = 3
                        else: 
                            dir = 4

            if score >= 0:
                lvl1 = True
            if dir == 0:
                speed_x = 0
                speed_y = 0
            if dir == 1:
                speed_x = 0
                speed_y = -15
            if dir == 2:
                speed_x = 0
                speed_y = 15
            if dir == 3:
                speed_y = 0
                speed_x = -15
            if dir == 4:
                speed_y = 0
                speed_x = 15

            snake_head = []
            player_x += speed_x
            player_y += speed_y

            snake_head.append(player_x)
            snake_head.append(player_y)
            snake_blocks.append(snake_head)

            collision = isCollision(apple_x, apple_y, player_x, player_y)

            if collision:
                apple_x = random.randrange(0,490, 5)
                apple_y = random.randrange(90,490, 5)
                score += 1
                snake_length += 1

            if len(snake_blocks) > snake_length:
                del snake_blocks[0]

            if player_x >= SCREEN_WIDTH or player_x < 0 or player_y >= SCREEN_HEIGHT or player_y < 90:
                game = False
                game_over = True

            score_label = Pixel20.render(f"Score: {str(score)}", 1, black)
            high_score_label = Pixel20.render(f"High Score: {str(highScore)}", 1, black)
            window.fill(white)
            window.blit(score_label, (0,0))
            window.blit(high_score_label, (0,50))
            pygame.draw.rect(window, red, (apple_x, apple_y, 10, 10))
            pygame.draw.rect(window, black, (0, 80, 500, 10), 3)
            for i in snake_blocks:
                pygame.draw.rect(window, black, pygame.Rect(i[0], i[1] ,10, 10))
            for i in snake_blocks[1:]:
                if snake_blocks[0][0] == i[0] and snake_blocks[0][1] == i[1]:
                    game = False
                    game_over = True
                    
            if lvl1:
                pass
            
            

        elif game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    if highScore < score:
                        with open("high_score.txt", "wb") as f:
                            pickle.dump(score, f)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        lvl1 = True
                        player_x = 240
                        player_y = 220
                        dir = 0
                        snake_length = 1
                        snake_blocks = []
                        score = 0
                        game_over = False
                        game = True
                        apple_x = random.randrange(0,490, 5)
                        apple_y = random.randrange(90,490, 5)
                        if highScore < score:
                            with open("high_score.txt", "wb") as f:
                                pickle.dump(score, f)

            window.fill(white)
            window.blit(game_over_label, (100,100))

            if highScore < score:
                with open("high_score.txt", "wb") as f:
                    pickle.dump(score, f)
    
            

        pygame.display.update()
        fps.tick(11)

if __name__ == "__main__":
    main()