import pygame
import random
from assets import hostile_bat_attacking_images, SCREEN_SIZE_X, level

class HostileBat(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.images = [pygame.transform.scale(img, (300, 300)) for img in hostile_bat_attacking_images]
        self.image = self.images[0]
        y_positions = [820, 600, 450] 
        self.rect = self.image.get_rect(midbottom=(SCREEN_SIZE_X + 50, random.choice(y_positions)))
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = 1000 // 5
        self.vitalis = 3 + level // 2


    def update(self):
        now = pygame.time.get_ticks()
        self.rect.x -= 5
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
        
        
        if self.rect.right < 0:
            self.kill()