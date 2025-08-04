import pygame
import json
import os

pygame.init()
pygame.mixer.init()



try:
    global mortanox_idle_image, mortanox_running_images, mortanox_attacking_images, mortanox_jumping_images
    global hostile_bat_moving_images, hostile_bat_attacking_images, mini_boss_moving_images
    global bg_image, vitalis_image, lucarius_image, vitalis_removed_image
    global overlay, attack_sound, lost_sound, attack_hit_sound, item_collected_sound
    global lucarii_path, lucarii_collected
    global SCREEN_SIZE_X, SCREEN_SIZE_Y
    SCREEN_SIZE_X = 1472
    SCREEN_SIZE_Y = 824
    global SCREEN_SIZE
    global width, height
        
    mortanox_idle_image = pygame.image.load("Assets/Player/MortanoxIdle.png")
    mortanox_running_images = [pygame.image.load(f"Assets/Player/Running/running{i}.png") for i in range(8)]
    mortanox_attacking_images = [pygame.image.load(f"Assets/Player/Attack/Attack{i}.png") for i in range(8)]
    mortanox_jumping_images = [pygame.image.load(f"Assets/Player/Jump/jump{i}.png") for i in range(12)]

    hostile_bat_moving_images = [pygame.image.load(f"Assets/Enemies/HostileBat/Moving/hostilebatmoving{i}.png") for i in range(4)]
    hostile_bat_attacking_images = [pygame.image.load(f"Assets/Enemies/HostileBat/Attack/hostilebat{i}.png") for i in range(8)]
    mini_boss_moving_images = [pygame.image.load(f"Assets/Enemies/MiniBoss/Moving/minibossmoving{i}.png") for i in range(4)]

    bg_image = pygame.image.load("Assets/World/UI/Images/BG.png").convert()
    vitalis_image = pygame.image.load("Assets/World/UI/Images/Vitalis.png")
    lucarius_image = pygame.image.load("Assets/World/UI/Images/Lucarius.png") 
    vitalis_removed_image = pygame.image.load("Assets/World/UI/VitalisRemovingAnimation/vitalis7.png")
        
        
    vitalis_removed_image = pygame.transform.scale(vitalis_removed_image, (70, 70))
    vitalis_image = pygame.transform.scale(vitalis_image, (70, 70))
    lucarius_image = pygame.transform.scale(lucarius_image, (70, 70))
        
    overlay = pygame.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
        
    pygame.mixer.music.load("Assets/World/UI/Sounds/BGMusic.wav")
    lost_sound = pygame.mixer.Sound("Assets/World/UI/Sounds/Lost.wav")
    attack_sound = pygame.mixer.Sound("Assets/World/UI/Sounds/Attack.wav")
    attack_hit_sound = pygame.mixer.Sound("Assets/World/UI/Sounds/AttackHit.wav")
    item_collected_sound = pygame.mixer.Sound("Assets/World/UI/Sounds/Collected.wav")
        
    pygame.mixer.music.set_volume(0.05)
    lost_sound.set_volume(0.3)
    attack_sound.set_volume(0.03)
    item_collected_sound.set_volume(0.2)
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

lucarii_path = "Assets/World/SaveFiles/Lucarii.json"
lucarii_collected = 0
bat_kill_count = 0
level_path = "Assets/World/SaveFiles/Level.json"

def save_lucarii():
    try:
        with open(lucarii_path, "w") as f:
            json.dump({"lucarii": lucarii_collected}, f)
    except IOError:
        pass

def save_level(level):
    with open("Assets/SaveFiles/level.json", "w") as f:
        json.dump({"level": level}, f)

def load_level():
    try:
        with open("Assets/SaveFiles/level.json", "r") as f:
            return json.load(f).get("level", 1)
    except FileNotFoundError:
        return 1
level = load_level()

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

