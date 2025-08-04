import pygame
import random
from assets import SCREEN_SIZE_X
lucarius_image = pygame.image.load("Assets/World/UI/Images/Lucarius.png")
class Lucarius(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = lucarius_image
        self.rect = self.image.get_rect(midbottom=(SCREEN_SIZE_X + 50, random.randint(600, 720)))
    
    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()