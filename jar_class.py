import pygame
import json
import os

class Jar:
    def __init__(self, effect: int, attribute: str, price: int, defect_attribute="", defect=0):
        self.bonus = effect
        self.attribute = attribute
        self.defect = defect
        self.defect_attribute = defect_attribute
        self.price = price
    
    def apply_positive(self, player):
        """Apply positive effects to the player"""
        if self.attribute.lower() == "speed":
            # Increase movement speed
            player.dx += self.bonus
        elif self.attribute.lower() == "health":
            # Heal the player (but don't exceed max health)
            player.vitalis = min(player.vitalis + self.bonus, player.max_vitalis)
        elif self.attribute.lower() == "max_health":
            # Increase maximum health and current health
            player.max_vitalis += self.bonus
            player.vitalis += self.bonus
        elif self.attribute.lower() == "jump_height":
            # Increase jump height
            player.jump_height += self.bonus
        elif self.attribute.lower() == "attack_speed":
            # Decrease attack cooldown (faster attacks)
            player.attack_cooldown = max(100, player.attack_cooldown - (self.bonus * 10))
        elif self.attribute.lower() == "second_chance":
            # Add a second chance mechanic (you'd need to implement this in the main game)
            player.second_chance = True
        elif self.attribute.lower() == "damage":
            # Increase damage
            player.damage += self.bonus
    
    def apply_negative(self, player):
        """Apply negative effects to the player"""
        if self.defect_attribute.lower() == "speed":
            player.dx = max(1, player.dx - self.defect)
        elif self.defect_attribute.lower() == "health":
            player.vitalis = max(1, player.vitalis - self.defect)
        elif self.defect_attribute.lower() == "max_health":
            player.max_vitalis = max(1, player.max_vitalis - self.defect)
            player.vitalis = min(player.vitalis, player.max_vitalis)
        elif self.defect_attribute.lower() == "jump_height":
            player.jump_height = max(5, player.jump_height - self.defect)
        elif self.defect_attribute.lower() == "attack_speed":
            player.attack_cooldown += (self.defect * 10)
        elif self.defect_attribute.lower() == "damage":
            player.damage = max(1, player.damage - self.defect)
    
    def apply(self, player):
        """Apply both positive and negative effects"""
        self.apply_positive(player)
        if self.defect_attribute:
            self.apply_negative(player)
    
    def buy(self, player):
        """Purchase the jar and apply its effects"""
        from assets import lucarii_collected, save_lucarii
        import assets
        
        if assets.lucarii_collected >= self.price:
            assets.lucarii_collected -= self.price
            self.apply(player)
            save_lucarii()
            return True
        else:
            print(f"Not enough Lucarii! Need {self.price}, have {assets.lucarii_collected}")
            return False