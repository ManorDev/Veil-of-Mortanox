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

        self.hitbox = pygame.Rect(0, 0, 150, 150)
        self.hitbox.center = self.rect.center

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = 1000 // 5
        self.vitalis = 3 + level // 2

        self.stunned = False
        self.stun_duration = 100
        self.stun_start_time = 0
        self.knockback_speed = 8 
        self.knockback_direction = -1

    def update(self):
        now = pygame.time.get_ticks()

        if self.stunned:
            if now - self.stun_start_time >= self.stun_duration:
                self.stunned = False  # end stun
            else:
                self.rect.x += self.knockback_speed * self.knockback_direction
                self.hitbox.center = self.rect.center
                return
        self.rect.x -= 5
        self.hitbox.center = self.rect.center

        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

        if self.rect.right < 0:
            self.kill()

    def get_hit(self, knockback_direction):
        if not self.stunned:
            self.stunned = True
            self.stun_start_time = pygame.time.get_ticks()
            self.knockback_direction = knockback_direction
            self.vitalis -= 1
            if self.vitalis <= 0:
                self.kill()
