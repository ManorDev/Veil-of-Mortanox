import pygame
import sys
import os
import subprocess
import json
from assets import lucarii_collected, lucarii_path, save_lucarii
from button_class import Button

pygame.init()
pygame.mixer.init()


screen_width, screen_height = 1000, 800
SCREEN_SIZE = (screen_width, screen_height)
screen = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("Menu")
FPS = pygame.time.Clock()

title_font = pygame.font.SysFont("Courier", 100, bold=True)
lucarius_font = pygame.font.SysFont("Courier", 45, bold=True)
button_font_size = 53

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)
HOVER_COLOR = (150, 150, 150)

lucarius_image = pygame.image.load("Assets/World/Images/Lucarius.png")
lucarius_image = pygame.transform.scale(lucarius_image, (100, 100))

title_text_surface = title_font.render("Menu", True, BLACK)
lucarius_text_surface = lucarius_font.render(str(lucarii_collected), True, BLACK)

play_button = Button(screen_width // 2 - 150, screen_height // 2 - 50, 300, 70)
shop_button = Button(screen_width // 2 - 150, screen_height // 2 + 50, 300, 70)
tutorial_button = Button(screen_width // 2 - 150, screen_height // 2 + 150, 300, 70)
quit_button = Button(screen_width // 2 - 150, screen_height // 2 + 250, 300, 70)

def main_menu():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if play_button.pressed():
            subprocess.call([sys.executable, "main.py"])
            pygame.quit()
            sys.exit()
        
        if shop_button.pressed():
            subprocess.call([sys.executable, "shop.py"])
            pygame.quit()
            sys.exit()
        
        if tutorial_button.pressed():
            subprocess.call([sys.executable, "tutorial.py"])
            pygame.quit()
            sys.exit()

        if quit_button.pressed():
            pygame.quit()
            sys.exit()

        screen.fill(WHITE)
        
        screen.blit(title_text_surface, (screen_width // 2 - title_text_surface.get_width() // 2, 50))
        screen.blit(lucarius_text_surface, (screen_width // 2 - lucarius_text_surface.get_width() // 2 - 272, 24))
        screen.blit(lucarius_image, (screen_width // 2 - lucarius_image.get_width() // 2 - 340, 0))

        play_button_color = HOVER_COLOR if play_button.pos[0] <= mouse_pos[0] <= play_button.pos[0] + play_button.w and play_button.pos[1] <= mouse_pos[1] <= play_button.pos[1] + play_button.h else BUTTON_COLOR
        shop_button_color = HOVER_COLOR if shop_button.pos[0] <= mouse_pos[0] <= shop_button.pos[0] + shop_button.w and shop_button.pos[1] <= mouse_pos[1] <= shop_button.pos[1] + shop_button.h else BUTTON_COLOR
        tutorial_button_color = HOVER_COLOR if tutorial_button.pos[0] <= mouse_pos[0] <= tutorial_button.pos[0] + tutorial_button.w and tutorial_button.pos[1] <= mouse_pos[1] <= tutorial_button.pos[1] + tutorial_button.h else BUTTON_COLOR
        quit_button_color = HOVER_COLOR if quit_button.pos[0] <= mouse_pos[0] <= quit_button.pos[0] + quit_button.w and quit_button.pos[1] <= mouse_pos[1] <= quit_button.pos[1] + quit_button.h else BUTTON_COLOR

        play_button.draw(screen, shape='rect', color=play_button_color, text='PLAY', text_color=WHITE, font_size=button_font_size, middle=True, border=True)
        shop_button.draw(screen, shape='rect', color=shop_button_color, text='SHOP', text_color=WHITE, font_size=button_font_size, middle=True, border=True)
        tutorial_button.draw(screen, shape='rect', color=tutorial_button_color, text='TUTORIAL', text_color=WHITE, font_size=button_font_size, middle=True, border=True)
        quit_button.draw(screen, shape='rect', color=quit_button_color, text='QUIT', text_color=WHITE, font_size=button_font_size, middle=True, border=True)
        
        pygame.display.flip()
        FPS.tick(60)

if __name__ == "__main__":
    main_menu()