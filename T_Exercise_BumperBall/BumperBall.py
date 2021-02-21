
import sys
import pygame

pygame.init()       # initialize pygame
size = (width, height) = (640, 480)     # Setting window
screen = pygame.display.set_mode(size)  # Display window
color = (0, 153, 204)   # Setting background color

ball = pygame.image.load("images/ball.png") # Load the picture and return a Surface object
ballrect = ball.get_rect()      # Get location

speed = [5, 5]  # Set x-axis and y-axis distance of the movement
clock = pygame.time.Clock() # setting clock

# Perform an endless loop to ensure that the window is always displayed
while True:
    clock.tick(60)  # 60 times per second
    # Check event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Confirm whether a QUIT event occurred
            sys.exit()

        ballrect = ballrect.move(speed)  # Moving ball

        # Hit the left and right edges
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        # Hit the top and bottom edges
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[-1]

        screen.fill(color)  # Fill color
        screen.blit(ball, ballrect) # Draw
        pygame.display.flip()# Update

pygame.quit()       # Exit pygame
