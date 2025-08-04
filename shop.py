import pygame
import subprocess
import sys
import os
import json
from button_class import Button
import assets
from assets import lucarii_collected, lucarii_path, save_lucarii
from jar_class import Jar
from player_class import create_mortanox

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 1200, 700
screen = pygame.display.set_mode((screen_width, screen_height))

def shop():
    pygame.display.set_caption("Shop")
    clock = pygame.time.Clock()

    BACKGROUND_COLOR = (26, 26, 46)
    BUTTON_NORMAL_COLOR = (50, 50, 70)
    BUTTON_HOVER_COLOR = (80, 80, 100)
    TEXT_COLOR = (255, 255, 255)
    TITLE_COLOR = (255, 215, 0)
    PRICE_COLOR = (180, 180, 200)
    SUCCESS_COLOR = (0, 255, 0)
    ERROR_COLOR = (255, 100, 100)

    lucarius_font = pygame.font.SysFont("Courier", 35)
    title_font = pygame.font.SysFont("Courier", 60, bold=True)
    jar_font = pygame.font.SysFont("Courier", 20, bold=True)
    message_font = pygame.font.SysFont("Courier", 24, bold=True)

    try:
        lucarius_image = pygame.image.load("Assets/World/Images/Lucarius.png").convert_alpha()
        lucarius_image = pygame.transform.scale(lucarius_image, (40, 40))
    except pygame.error:
        lucarius_image = pygame.Surface((40, 40))
        lucarius_image.fill((255, 215, 0))

    button_width, button_height = 150, 150
    spacing = 50
    start_x, start_y = 50, 150

    # Create buttons
    damage_button = Button(start_x, start_y, button_width, button_height)
    health_button = Button(start_x + button_width + spacing, start_y, button_width, button_height)
    speed_button = Button(start_x + 2 * (button_width + spacing), start_y, button_width, button_height)
    jump_height_button = Button(start_x + 3 * (button_width + spacing), start_y, button_width, button_height)
    
    second_chance_button = Button(start_x, start_y + button_height + spacing, button_width, button_height)
    max_health_button = Button(start_x + button_width + spacing, start_y + button_height + spacing, button_width, button_height)
    attack_speed_button = Button(start_x + 2 * (button_width + spacing), start_y + button_height + spacing, button_width, button_height)

    button_list = [damage_button, health_button, speed_button, jump_height_button, 
                   second_chance_button, max_health_button, attack_speed_button]
    
    button_texts = ["Power Jar", "Health Jar", "Speed Jar", "Jump Boost", 
                   "Second Chance", "Max Health", "Attack Speed"]
    jars_list = [
        Jar(1, "damage", 30),           
        Jar(1, "health", 50),             
        Jar(2, "speed", 30),            
        Jar(5, "jump_height", 20),      
        Jar(1, "second_chance", 200),   
        Jar(1, "max_health", 150),      
        Jar(50, "attack_speed", 80)    
    ]
    
    shop_lucarii_count = assets.lucarii_collected
    
    mortanox = create_mortanox()
    

    message_text = ""
    message_color = TEXT_COLOR
    message_timer = 0
    
    shopping = True
    while shopping:
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                assets.lucarii_collected = shop_lucarii_count
                save_lucarii()
                pygame.quit()
                subprocess.call([sys.executable, "menu.py"])
                sys.exit()
                shopping = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    assets.lucarii_collected = shop_lucarii_count
                    save_lucarii()
                    pygame.quit()
                    subprocess.call([sys.executable, "menu.py"])
                    sys.exit()
                    shopping = False

        screen.fill(BACKGROUND_COLOR)
        
        title_surface = title_font.render("Shop", True, TITLE_COLOR)
        screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 20))
        
        lucarii_surface = lucarius_font.render(str(shop_lucarii_count), True, TEXT_COLOR)
        screen.blit(lucarius_image, (screen_width - 100, 20))
        screen.blit(lucarii_surface, (screen_width - 50, 25))

        for i, button in enumerate(button_list):
            button_color = BUTTON_NORMAL_COLOR
            if button.is_hovered():
                button_color = BUTTON_HOVER_COLOR

            if button.pressed():
                jar = jars_list[i]
                if shop_lucarii_count >= jar.price:
                    shop_lucarii_count -= jar.price
                    jar.apply(mortanox)
                    message_text = f"Purchased {button_texts[i]}!"
                    message_color = SUCCESS_COLOR
                    message_timer = current_time + 2000
                else:
                    message_text = f"Not enough Lucarii! Need {jar.price}"
                    message_color = ERROR_COLOR
                    message_timer = current_time + 2000
            
            button.draw(screen, 'rect', button_color, button_texts[i], TEXT_COLOR, 16, True, TEXT_COLOR, True)
            
            price_text = f"Cost: {jars_list[i].price}"
            price_surface = jar_font.render(price_text, True, PRICE_COLOR)
            price_x = button.pos[0] + button.w // 2 - price_surface.get_width() // 2
            price_y = button.pos[1] + button.h + 5
            screen.blit(price_surface, (price_x, price_y))

        if message_timer > current_time and message_text:
            message_surface = message_font.render(message_text, True, message_color)
            message_x = screen_width // 2 - message_surface.get_width() // 2
            message_y = screen_height - 100
            screen.blit(message_surface, (message_x, message_y))

        instruction_text = "Press ESC to exit shop"
        instruction_surface = jar_font.render(instruction_text, True, PRICE_COLOR)
        instruction_x = screen_width // 2 - instruction_surface.get_width() // 2
        instruction_y = screen_height - 50
        screen.blit(instruction_surface, (instruction_x, instruction_y))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    subprocess.call([sys.executable, "menu.py"])
    sys.exit()

if __name__ == "__main__":
    shop()