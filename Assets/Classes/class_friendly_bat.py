import pygame
from assets import SCREEN_SIZE_X

class FriendlyBat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bat_images = [pygame.image.load(f"Assets/World/Bat/bat{i}.png") for i in range(4)]
        self.images = [pygame.transform.scale(img, (80, 60)) for img in bat_images]
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=(SCREEN_SIZE_X + 50, 640))
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = 1000 // 8

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
        
        self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()