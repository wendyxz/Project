'''
Function:

   Define the dropped items such as golden eggs

'''
import pygame
import random


'''Define food group'''
class Food(pygame.sprite.Sprite):
    def __init__(self, images_dict, selected_key, screensize, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.screensize = screensize
        self.image = images_dict[selected_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = random.randint(20, screensize[0]-20), -10
        self.speed = random.randrange(5, 10)
        self.score = 1 if selected_key == 'egg' else 5
    '''Update food location'''
    def update(self):
        self.rect.bottom += self.speed
        if self.rect.top > self.screensize[1]:
            return True
        return False
