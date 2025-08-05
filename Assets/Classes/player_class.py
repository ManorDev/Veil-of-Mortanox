import pygame

pygame.init()
pygame.mixer.init()

SCREEN_SIZE_X = 1472  
SCREEN_SIZE_Y = 824
SCREEN_SIZE = (SCREEN_SIZE_X, SCREEN_SIZE_Y)

class Mortanox(pygame.sprite.Sprite):
    def __init__(self, max_vitalis=5):
        super().__init__()
        
        try:
            from assets import (mortanox_idle_image, mortanox_running_images, 
                              mortanox_attacking_images, mortanox_jumping_images, attack_sound)
            
            self.idle_image = pygame.transform.scale(mortanox_idle_image, (200, 100))
            self.running_images = [pygame.transform.scale(img, (200, 100)) for img in mortanox_running_images]
            self.attacking_images = [pygame.transform.scale(img, (200, 100)) for img in mortanox_attacking_images]
            self.jumping_images = [pygame.transform.scale(img, (200, 100)) for img in mortanox_jumping_images]
            self.attack_sound = attack_sound
        except ImportError:
            self.idle_image = pygame.Surface((200, 100))
            self.idle_image.fill((255, 0, 0))
            self.running_images = [self.idle_image] * 8
            self.attacking_images = [self.idle_image] * 8
            self.jumping_images = [self.idle_image] * 12
            self.attack_sound = None
        
        self.damage = 3
        

        self.vitalis_removed_image = [pygame.transform.scale(pygame.image.load(f"Assets/World/UI/VitalisRemovingAnimation/vitalis{i}.png"), (70, 70)) for i in range(8)]
        self.vitalis = max_vitalis
        self.max_vitalis = max_vitalis
        self.vitalis_animating = False
        self.vitalis_anim_frame = 0
        self.vitalis_anim_start_time = 0
        self.vitalis_anim_speed = 50

        self.jump_height = 20
        self.base_speed = 5
        self.speed_bonus = 0  
        
        self.is_running = False
        self.is_jumping = False
        self.is_attacking = False
        self.second_chance = False  # For second chance jar
        self.has_used_second_chance = False
        
        self.attack_cooldown = 500
        self.last_attack_time = 0
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 13
        self.frame_duration = 1000 // self.animation_speed
        
        self.image = self.idle_image
        self.rect = self.image.get_rect(midbottom=(100, 750))
        
        self.dx = 0
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.last_attack_hit_time = 0
        
        self.inventory = ["Gladius Umbrae",0,0,0]
    
    def fill_inv(self, item):
        for i in range(4):
            if self.inventory[i]!=0:
                self.inventory[i] = item
                return True
        return False  # Inventory full
    def repalce(self,place,element):
        self.inventory[place]=element
    def delete(self,place):
        self.inventory[place]=0
    def get_current_speed(self):
        return self.base_speed + self.speed_bonus
    
    def update(self):
        self.animate()

        if self.vitalis_animating:
            now = pygame.time.get_ticks()
            if now - self.vitalis_anim_start_time > self.vitalis_anim_speed:
                self.vitalis_anim_start_time = now
                self.vitalis_anim_frame += 1
                if self.vitalis_anim_frame >= len(self.vitalis_removed_image):
                    self.vitalis_animating = False
                    self.vitalis_anim_frame = 0

        if not self.is_attacking:
            self.rect.x += self.dx
        
        if not self.on_ground:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            if self.rect.bottom >= 750:
                self.rect.bottom = 750
                self.on_ground = True
                self.is_jumping = False
                self.velocity_y = 0
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_SIZE_X:
            self.rect.right = SCREEN_SIZE_X
    
    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            
            if self.is_attacking:
                self.current_frame = (self.current_frame + 1) % len(self.attacking_images)
                self.image = self.attacking_images[self.current_frame]
                if self.current_frame == len(self.attacking_images) - 1:
                    self.is_attacking = False
            
            elif self.is_jumping:
                if self.velocity_y < 0 and self.current_frame < len(self.jumping_images) - 1:
                    self.current_frame = (self.current_frame + 1)
                self.image = self.jumping_images[min(self.current_frame, len(self.jumping_images) - 1)]
            
            elif self.is_running:
                self.current_frame = (self.current_frame + 1) % len(self.running_images)
                self.image = self.running_images[self.current_frame]
            
            else:
                self.current_frame = 0
                self.image = self.idle_image
    
    def run(self, direction):
        self.is_running = True
        self.dx = self.get_current_speed() * direction
    
    def stop(self):
        self.is_running = False
        self.dx = 0
        self.current_frame = 0
    
    def jump(self):
        if self.on_ground and not self.is_attacking:
            self.on_ground = False
            self.is_jumping = True
            self.velocity_y = -self.jump_height
            self.current_frame = 0
    
    def attack(self):
        current_time = pygame.time.get_ticks()
        if not self.is_attacking and current_time - self.last_attack_time >= self.attack_cooldown:
            self.is_attacking = True
            self.current_frame = 0
            self.last_attack_time = current_time
            if self.attack_sound:
                self.attack_sound.play()
    
    def get_attack_rect(self):
        if self.is_attacking:
            attack_width = 70
            attack_height = 50
            return pygame.Rect(self.rect.right - 20, self.rect.y + 20, attack_width, attack_height)
        return None
    
    def take_damage(self, damage=1):
        if self.vitalis > 0:
            self.vitalis -= damage
            self.vitalis_animating = True
            self.vitalis_anim_frame = 0
            self.vitalis_anim_start_time = pygame.time.get_ticks()

        
        if self.vitalis <= 0 and self.second_chance and not self.has_used_second_chance:
            self.vitalis = 1
            self.second_chance = False
            self.has_used_second_chance = True
            print("Second chance activated!")
            return False
        
        return self.vitalis <= 0
    
    def heal(self, amount):
        """Heal the player"""
        self.vitalis = min(self.vitalis + amount, self.max_vitalis)
    
    def increase_max_health(self, amount):
        self.max_vitalis += amount
        self.heal(amount)
    
    def increase_damage(self, amount):
        self.damage += amount
    
    def increase_speed(self, amount):
        self.speed_bonus += amount
    
    def increase_jump_height(self, amount):
        self.jump_height += amount
    
    def decrease_attack_cooldown(self, amount):
        self.attack_cooldown = max(100, self.attack_cooldown - amount)

def create_mortanox():
    return Mortanox()