
import os
import cfg
import sys
import pygame
import random
from modules import *


'''Game initialization'''
def initGame():
    # Initialize pygame, set the display window
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('catch gift ')
    # Load game material
    game_images = {}
    for key, value in cfg.IMAGE_PATHS.items():
        if isinstance(value, list):
            images = []
            for item in value: images.append(pygame.image.load(item))
            game_images[key] = images
        else:
            game_images[key] = pygame.image.load(value)
    game_sounds = {}
    for key, value in cfg.AUDIO_PATHS.items():
        if key == 'bgm': continue
        game_sounds[key] = pygame.mixer.Sound(value)
    # Return initialization data
    return screen, game_images, game_sounds


'''Main function'''
def main():
    # initialization
    screen, game_images, game_sounds = initGame()
    # Play background music
    pygame.mixer.music.load(cfg.AUDIO_PATHS['bgm'])
    pygame.mixer.music.play(-1, 0.0)
    # Font loading
    font = pygame.font.Font(cfg.FONT_PATH, 40)
    # Define hero
    hero = Hero(game_images['hero'], position=(375, 520))
    # Define food group
    food_sprites_group = pygame.sprite.Group()
    generate_food_freq = random.randint(10, 20)
    generate_food_count = 0
    # Current score/Highest score in history
    score = 0
    highest_score = 0 if not os.path.exists(cfg.HIGHEST_SCORE_RECORD_FILEPATH) else int(open(cfg.HIGHEST_SCORE_RECORD_FILEPATH).read())
    # Main loop
    clock = pygame.time.Clock()
    while True:
        # --Fill background
        screen.fill(0)
        screen.blit(game_images['background'], (0, 0))
        # --Countdown information
        countdown_text = 'Count down: ' + str((90000 - pygame.time.get_ticks()) // 60000) + ":" + str((90000 - pygame.time.get_ticks()) // 1000 % 60).zfill(2)
        countdown_text = font.render(countdown_text, True, (0, 0, 0))
        countdown_rect = countdown_text.get_rect()
        countdown_rect.topright = [cfg.SCREENSIZE[0]-30, 5]
        screen.blit(countdown_text, countdown_rect)
        # --Button detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            hero.move(cfg.SCREENSIZE, 'left')
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            hero.move(cfg.SCREENSIZE, 'right')
        # --Randomly generate food
        generate_food_count += 1
        if generate_food_count > generate_food_freq:
            generate_food_freq = random.randint(10, 20)
            generate_food_count = 0
            food = Food(game_images, random.choice(['egg',] * 10 + ['love']), cfg.SCREENSIZE)
            food_sprites_group.add(food)
        # --Update food
        for food in food_sprites_group:
            if food.update(): food_sprites_group.remove(food)
        # --Impact checking
        for food in food_sprites_group:
            if pygame.sprite.collide_mask(food, hero):
                game_sounds['get'].play()
                food_sprites_group.remove(food)
                score += food.score
                if score > highest_score: highest_score = score
        # --Draw hero
        hero.draw(screen)
        # --Draw food
        food_sprites_group.draw(screen)
        # --Display score
        score_text = f'Score: {score}, Highest: {highest_score}'
        score_text = font.render(score_text, True, (0, 0, 0))
        score_rect = score_text.get_rect()
        score_rect.topleft = [5, 5]
        screen.blit(score_text, score_rect)
        # --Determine if the game is over
        if pygame.time.get_ticks() >= 90000:
            break
        # --Update screen
        pygame.display.flip()
        clock.tick(cfg.FPS)
    # Game over, record the highest score and display the game over screen
    fp = open(cfg.HIGHEST_SCORE_RECORD_FILEPATH, 'w')
    fp.write(str(highest_score))
    fp.close()
    return showEndGameInterface(screen, cfg, score, highest_score)


'''run'''
if __name__ == '__main__':
    while main():
        pass
