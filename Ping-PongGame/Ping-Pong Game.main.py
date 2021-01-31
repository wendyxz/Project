'''
Function:
    Ping-Pong Game

'''
import sys
import cfg
import pygame
from modules import *


'''Define Button'''
def Button(screen, position, text, button_size=(200, 50)):
    left, top = position
    bwidth, bheight = button_size
    pygame.draw.line(screen, (150, 150, 150), (left, top), (left+bwidth, top), 5)
    pygame.draw.line(screen, (150, 150, 150), (left, top-2), (left, top+bheight), 5)
    pygame.draw.line(screen, (50, 50, 50), (left, top+bheight), (left+bwidth, top+bheight), 5)
    pygame.draw.line(screen, (50, 50, 50), (left+bwidth, top+bheight), (left+bwidth, top), 5)
    pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
    font = pygame.font.Font(cfg.FONTPATH, 30)
    text_render = font.render(text, 1, (255, 235, 205))
    return screen.blit(text_render, (left+50, top+10))


'''
Function:
    Start Interface
Input:
    --screen: Game Interface
Return:
    --game_mode: 1 player/2 players
'''
def startInterface(screen):
    clock = pygame.time.Clock()
    while True:
        screen.fill((41, 36, 33))
        button_1 = Button(screen, (150, 175), '1 Player')
        button_2 = Button(screen, (150, 275), '2 Player')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    return 1
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    return 2
        clock.tick(10)
        pygame.display.update()


'''End Interface'''
def endInterface(screen, score_left, score_right):
    clock = pygame.time.Clock()
    font1 = pygame.font.Font(cfg.FONTPATH, 30)
    font2 = pygame.font.Font(cfg.FONTPATH, 20)
    msg = 'Player on left won!' if score_left > score_right else 'Player on right won!'
    texts = [font1.render(msg, True, cfg.WHITE),
            font2.render('Press ESCAPE to quit.', True, cfg.WHITE),
            font2.render('Press ENTER to continue or play again.', True, cfg.WHITE)]
    positions = [[120, 200], [155, 270], [80, 300]]
    while True:
        screen.fill((41, 36, 33))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
        for text, pos in zip(texts, positions):
            screen.blit(text, pos)
        clock.tick(10)
        pygame.display.update()


'''Run the Game Demo'''
def runDemo(screen):
    # Load Game Material
    hit_sound = pygame.mixer.Sound(cfg.HITSOUNDPATH)
    goal_sound = pygame.mixer.Sound(cfg.GOALSOUNDPATH)
    font = pygame.font.Font(cfg.FONTPATH, 50)
    # Start Interface
    game_mode = startInterface(screen)
    # Main Loop
    # --Left Racket (ws control, only for 2 Player)
    score_left = 0
    racket_left = Racket(cfg.RACKETPICPATH, 'LEFT', cfg)
    # --Right Racket(↑↓ control)
    score_right = 0
    racket_right = Racket(cfg.RACKETPICPATH, 'RIGHT', cfg)
    # --Ball
    ball = Ball(cfg.BALLPICPATH, cfg)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)
        screen.fill((41, 36, 33))
        # Player Action
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP]:
            racket_right.move('UP')
        elif pressed_keys[pygame.K_DOWN]:
            racket_right.move('DOWN')
        if game_mode == 2:
            if pressed_keys[pygame.K_w]:
                racket_left.move('UP')
            elif pressed_keys[pygame.K_s]:
                racket_left.move('DOWN')
        else:
            racket_left.automove(ball)
        # Ball Movement
        scores = ball.move(ball, racket_left, racket_right, hit_sound, goal_sound)
        score_left += scores[0]
        score_right += scores[1]
        # Display
        # --Divider
        pygame.draw.rect(screen, cfg.WHITE, (247, 0, 6, 500))
        # --Ball
        ball.draw(screen)
        # --Racket
        racket_left.draw(screen)
        racket_right.draw(screen)
        # --Score
        screen.blit(font.render(str(score_left), False, cfg.WHITE), (150, 10))
        screen.blit(font.render(str(score_right), False, cfg.WHITE), (300, 10))
        if score_left == 11 or score_right == 11:
            return score_left, score_right
        clock.tick(100)
        pygame.display.update()


'''Main'''
def main():
    # initialization
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pygame.display.set_caption('Ping-Pong Game ')
    # Start the Game
    while True:
        score_left, score_right = runDemo(screen)
        endInterface(screen, score_left, score_right)


'''run'''
if __name__ == '__main__':
    main()
