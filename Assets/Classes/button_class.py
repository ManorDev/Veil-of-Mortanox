import pygame
import math

class Button:
    pygame.font.init()
    
    def __init__(self, x, y, w, h):
        self.pos = (x, y)
        self.w = w
        self.h = h
        self.size = (w, h)
        self.rect_draw = (x, y, w, h)
        self.original_size = (w, h)
    
    def draw(self, window, shape='rect', color=(255, 255, 255), text='', text_color=(255, 255, 255), 
             font_size=10, middle=False, border_color=(0, 0, 0), border=True):
        """Draw the button on the window"""
        if border:
            if shape == 'rect':
                pygame.draw.rect(window, border_color, 
                               (self.pos[0] - 1, self.pos[1] - 1, self.size[0] + 2, self.size[1] + 2))
            else:
                pygame.draw.circle(window, border_color, self.pos, self.size[0] + 3)
        
        if shape == 'rect':
            pygame.draw.rect(window, color, self.rect_draw)
        else:
            pygame.draw.circle(window, color, self.pos, self.size[0])
        if text:
            text_font = pygame.font.SysFont("Courier", font_size, bold=True)
            text_surface = text_font.render(text, True, text_color)
            
            if shape == 'rect':
                button_rect = pygame.Rect(self.pos[0], self.pos[1], self.w, self.h)
                text_rect = text_surface.get_rect(center=button_rect.center)
            else:
                text_rect = text_surface.get_rect(center=self.pos)
            
            window.blit(text_surface, text_rect)
    
    def pressed(self, shape='rect'):
        pos = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()
        
        if shape == 'rect':
            if (press[0] and 
                self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and 
                self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]):
                return True
            return False
        else:
            # For circular buttons
            x = pos[0] - self.pos[0]
            y = pos[1] - self.pos[1]
            if math.sqrt(x**2 + y**2) <= self.size[0] and press[0]:
                return True
            return False
    
    def is_hovered(self, shape='rect'):
        pos = pygame.mouse.get_pos()
        
        if shape == 'rect':
            return (self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and 
                   self.pos[1] <= pos[1] <= self.pos[1] + self.size[1])
        else:
            x = pos[0] - self.pos[0]
            y = pos[1] - self.pos[1]
            return math.sqrt(x**2 + y**2) <= self.size[0]
    
    def layered(self, window, shape, ori_color, num=8, color=(255, 255, 255)):
        self.size = list(self.size)
        
        for i in range(num // 2):
            self.draw(window, shape, ori_color, '', (0, 0, 0), 10, False, (0, 0, 0), False)
            self.size[1] -= 8
            self.size[0] -= 8
            self.draw(window, shape, color, '', (0, 0, 0), 10, False, (0, 0, 0), False)
            self.size[1] -= 8
            self.size[0] -= 8
    
    def return_normal_size(self):
        self.size = self.original_size