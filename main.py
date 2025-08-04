import os
import json
import random
import pygame
import subprocess
import sys

from lucarius_class import Lucarius
from hostile_bat_class import HostileBat
from class_friendly_bat import FriendlyBat
from player_class import Mortanox
from button_class import Button
from assets import lucarii_path, lucarii_collected, save_lucarii, save_level, level_path, level, load_level, bat_kill_count

pygame.init()
pygame.mixer.init()

SCREEN_SIZE_X = 1472
SCREEN_SIZE_Y = 824
screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
pygame.display.set_caption("Veil of Mortanox")
clock = pygame.time.Clock()

try:
    mortanox_idle_image = pygame.image.load("Assets/Player/MortanoxIdle.png")
    mortanox_running_images = [pygame.image.load(f"Assets/Player/Running/running{i}.png") for i in range(8)], (70, 70)
    mortanox_attacking_images = [pygame.image.load(f"Assets/Player/Attack/Attack{i}.png") for i in range(8)]
    mortanox_jumping_images = [pygame.image.load(f"Assets/Player/Jump/jump{i}.png") for i in range(12)]

    hostile_bat_moving_images = [pygame.image.load(f"Assets/Enemies/HostileBat/Moving/hostilebatmoving{i}.png") for i in range(4)]
    hostile_bat_attacking_images = [pygame.image.load(f"Assets/Enemies/HostileBat/Attack/hostilebat{i}.png") for i in range(8)]
    mini_boss_moving_images = [pygame.image.load(f"Assets/Enemies/MiniBoss/Moving/minibossmoving{i}.png") for i in range(4)]

    bg_image = pygame.image.load("Assets/World/UI/Images/BG.png").convert()
    vitalis_image = pygame.image.load("Assets/World/UI/Images/Vitalis.png")
    lucarius_image = pygame.image.load("Assets/World/UI/Images/Lucarius.png") 
    vitalis_removed_image = [pygame.image.load(f"Assets/World/UI/VitalisRemovingAnimation/vitalis{i}.png") for i in range(8)]
        
        
    vitalis_removed_image = [pygame.transform.scale(pygame.image.load(f"Assets/World/UI/VitalisRemovingAnimation/vitalis{i}.png"), (70, 70)) for i in range(8)]
    vitalis_image = pygame.transform.scale(vitalis_image, (70, 70))
    lucarius_image = pygame.transform.scale(lucarius_image, (70, 70))
        
    overlay = pygame.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
        
    pygame.mixer.music.load("Assets/World/UI/Sounds/BGMusic.wav")
    lost_sound = pygame.mixer.Sound("Assets/World/UI/Sounds/Lost.wav")
    attack_sound = pygame.mixer.Sound("Assets/World/UI/Sounds/Attack.wav")
    attack_hit_sound = pygame.mixer.Sound("Assets/World/UI/Sounds/AttackHit.wav")
    item_collected_sound = pygame.mixer.Sound("Assets/World/UI/Sounds/Collected.wav")
        
    pygame.mixer.music.set_volume(0.5)
    lost_sound.set_volume(0.5)
    attack_sound.set_volume(0.5)
    attack_hit_sound.set_volume(0.5)
    item_collected_sound.set_volume(0.5)
    pygame.mixer.music.play(-1)

except pygame.error as e:
    print(f"Failed to load assets or sounds: {e}")
    class DummySound:
        def play(self, loops=0): pass
        def set_volume(self, vol): pass
    
    lost_sound = DummySound()
    attack_sound = DummySound()
    attack_hit_sound = DummySound()
    item_collected_sound = DummySound()

font = pygame.font.SysFont("Courier", 40,)
game_over_font = pygame.font.SysFont("Courier", 60, bold=True)
game_over = False


if os.path.exists(lucarii_path):
    try:
        with open(lucarii_path, "r") as f:
            data = json.load(f)
            if data and isinstance(data, dict):
                lucarii_collected = data.get("lucarii", 0)
                if not isinstance(lucarii_collected, int):
                    lucarii_collected = 0
    except (json.JSONDecodeError, IOError, KeyError):
        lucarii_collected = 0

if os.path.exists(level_path):
    try:
        with open(level_path, "r") as f:
            data = json.load(f)
            if data and isinstance(data, dict):
                level = data.get("Level", 1)
                if not isinstance(level, int):
                    level = 1
    except (json.JSONDecodeError, IOError, KeyError):
        level = 1

all_sprites = pygame.sprite.Group()
lucarii_group = pygame.sprite.Group()
hostile_bats_group = pygame.sprite.Group()
friendly_bats_group = pygame.sprite.Group()

def spawn_lucarius():
    lucarius = Lucarius()
    all_sprites.add(lucarius)
    lucarii_group.add(lucarius)

def spawn_hostile_bat():
    bat = HostileBat()
    all_sprites.add(bat)
    hostile_bats_group.add(bat)

def spawn_friendly_bat():
    bat = FriendlyBat()
    all_sprites.add(bat)
    friendly_bats_group.add(bat)

def game_over_screen():
    global game_over, lucarii_collected
    pygame.mixer.music.stop()
    lost_sound.play()
    
    BUTTON_NORMAL_COLOR = (255, 0, 255)
    BUTTON_HOVER_COLOR = (200, 0, 200)
    
    menu_button = Button(SCREEN_SIZE_X / 2 - 175, SCREEN_SIZE_Y / 2 + 50, 350, 60)
    exit_button = Button(SCREEN_SIZE_X / 2 - 175, SCREEN_SIZE_Y / 2 + 150, 350, 60)
    
    while game_over:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_level()
                save_lucarii()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    save_level()
                    save_lucarii()
                    pygame.quit()
                    subprocess.call([sys.executable, "menu.py"])
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    save_level()
                    save_lucarii()
                    pygame.quit()
                    sys.exit()

        if menu_button.pressed():
            save_level()
            save_lucarii()
            pygame.quit()
            subprocess.call([sys.executable, "menu.py"])
            sys.exit()
        if exit_button.pressed():
            save_level()
            save_lucarii()
            pygame.quit()
            sys.exit()

        screen.blit(overlay, (0, 0))

        menu_button_color = BUTTON_NORMAL_COLOR
        if menu_button.pos[0] <= mouse_pos[0] <= menu_button.pos[0] + menu_button.w and menu_button.pos[1] <= mouse_pos[1] <= menu_button.pos[1] + menu_button.h:
            menu_button_color = BUTTON_HOVER_COLOR

        exit_button_color = BUTTON_NORMAL_COLOR
        if exit_button.pos[0] <= mouse_pos[0] <= exit_button.pos[0] + exit_button.w and exit_button.pos[1] <= mouse_pos[1] <= exit_button.pos[1] + exit_button.h:
            exit_button_color = BUTTON_HOVER_COLOR

        menu_button.draw(screen, "rect", menu_button_color, "Menu - M", (255, 255, 255), 40, False, (255, 255, 255), True)
        exit_button.draw(screen, "rect", exit_button_color, "Exit - ESC", (255, 255, 255), 40, False, (255, 255, 255), True)

        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 255))
        text_rect = game_over_text.get_rect(center=(SCREEN_SIZE_X / 2, SCREEN_SIZE_Y / 2 - 100))
        screen.blit(game_over_text, text_rect)
        
        pygame.display.update()
        clock.tick(60)

def create_mortanox():
    global mortanox
    mortanox = Mortanox()
def main_game_loop():
    global lucarii_collected, game_over, bat_kill_count
    create_mortanox()
    all_sprites.empty()
    lucarii_group.empty()
    hostile_bats_group.empty()
    friendly_bats_group.empty()
    
    all_sprites.add(mortanox)
    
    bg1_x, bg1_y = 0, 0
    bg2_x = bg_image.get_width()
    
    lucarii_time = pygame.time.get_ticks() + random.randint(5000, 7000)
    hostile_bat_time = pygame.time.get_ticks() + 5000
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        mortanox.jump()
                    if event.key == pygame.K_x:
                        attack_sound.play()
                        mortanox.attack()
                    if event.key == pygame.K_RIGHT:
                        mortanox.run(1)
                    if event.key == pygame.K_LEFT:
                        mortanox.run(-1)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        mortanox.stop()
        
        if not game_over:
            current_time = pygame.time.get_ticks()
            bg1_x -= 2
            bg2_x -= 2
            if bg1_x + bg_image.get_width() <= 0:
                bg1_x = bg2_x + bg_image.get_width()
            if bg2_x + bg_image.get_width() <= 0:
                bg2_x = bg1_x + bg_image.get_width()
            
            if current_time >= lucarii_time:
                spawn_lucarius()
                lucarii_time = current_time + random.randint(1500, 2000)
            
            if current_time >= hostile_bat_time:
                spawn_hostile_bat()
                hostile_bat_time = current_time + 1500
            
            all_sprites.update()
            
            if mortanox.is_attacking and mortanox.current_frame == 4 and pygame.time.get_ticks() - mortanox.last_attack_hit_time > 400:
                mortanox.last_attack_hit_time = pygame.time.get_ticks()
                attack_rect = mortanox.get_attack_rect()
                if attack_rect:
                    hit_bats = [bat for bat in hostile_bats_group if attack_rect.colliderect(bat.hitbox)]
                    for bat in hit_bats:
                        attack_hit_sound.play()
                        knockback_direction = 1 if mortanox.rect.centerx < bat.rect.centerx else -1
                        bat.get_hit(knockback_direction)
    
                        if bat.vitalis <= 0:
                            bat.kill()
                            bat_kill_count += 1
                            lucarii_collected += random.randint(5, 15)
                            item_collected_sound.play()

                                

            
            collected_lucarii = pygame.sprite.spritecollide(mortanox, lucarii_group, True, pygame.sprite.collide_rect)
            for _ in collected_lucarii:
                item_collected_sound.play()
                lucarii_collected += 1
            
            collided_bats = [bat for bat in hostile_bats_group if mortanox.rect.colliderect(bat.hitbox)]
            if collided_bats:
                if not mortanox.vitalis_animating:
                    mortanox.vitalis -= 1
                    mortanox.vitalis_animating = True
                    mortanox.vitalis_anim_frame = 0
                    mortanox.vitalis_anim_start_time = pygame.time.get_ticks()
                if mortanox.vitalis <= 0:
                    game_over = True
                    run = False
        
        
        screen.blit(bg_image, (bg1_x, bg1_y))
        screen.blit(bg_image, (bg2_x, bg1_y))
        

        all_sprites.draw(screen)
        for bat in hostile_bats_group:
            bar_width = 60
            bar_height = 10
            bar_x = bat.rect.centerx - bar_width // 2
            bar_y = bat.rect.top - 20
            max_health = 3 + level // 2
            fill = (bat.vitalis / max_health) * bar_width
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill, bar_height))
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        screen.blit(lucarius_image, (10, 10))
        coin_text = font.render(str(lucarii_collected), True, (255, 255, 255))
        screen.blit(coin_text, (80, 23))


        for i in range(mortanox.vitalis):
            screen.blit(vitalis_image, (10 + i * 45, 70))


        if mortanox.vitalis_animating and mortanox.vitalis_anim_frame < len(mortanox.vitalis_removed_image):
            frame = mortanox.vitalis_removed_image[mortanox.vitalis_anim_frame]
            screen.blit(frame, (10 + mortanox.vitalis * 45, 70))


        
        pygame.display.update()
        clock.tick(60)

    save_lucarii()
    if game_over:
        game_over_screen()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_game_loop()