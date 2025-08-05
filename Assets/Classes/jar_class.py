from player_class import Mortanox

class Jar:
    def __init__(self, effect: int, attribute: str, price: int, defect_attribute="", defect=0,duration=-1):
        self.bonus = effect
        self.attribute = attribute
        self.defect = defect
        self.defect_attribute = defect_attribute
        self.price = price
        self.duration=duration
        self.in_effect=False
        self.attack_speed = 1
        self.used_duration = 0
    def apply_positive(self, mortanox,offset=1):
        assert type(mortanox) == Mortanox
        """Apply positive effects to the mortanox"""
        if not self.in_effect:
            if self.attribute.lower() == "speed":
                mortanox.dx += offset*(self.bonus)
            elif self.attribute.lower() == "health":
                mortanox.vitalis += min(mortanox.vitalis + self.bonus, mortanox.max_vitalis)
            elif self.attribute.lower() == "max_health":
                mortanox.max_vitalis += self.bonus
                mortanox.vitalis += self.bonus
            elif self.attribute.lower() == "jump_height":
                mortanox.jump_height += offset*(self.bonus)
            elif self.attribute.lower() == "attack_speed":
                if offset==1:
                    self.attack_speed=mortanox.attack_cooldown
                    mortanox.attack_cooldown = max(100, mortanox.attack_cooldown - (self.bonus * 10))
                else:
                    mortanox.attack_cooldown=self.attack_speed
            elif self.attribute.lower() == "second_chance":
                mortanox.second_chance = True
            elif self.attribute.lower() == "damage":
                mortanox.damage += offset(self.bonus)
                self.effect=True
    
    def apply_neve(self, mortanox):
        assert type(mortanox) == Mortanox
        """Apply negative effects to the mortanox"""
        if self.defect_attribute.lower() == "speed":
            mortanox.dx = max(1, mortanox.dx - self.defect)
        elif self.defect_attribute.lower() == "health":
            mortanox.vitalis = max(1, mortanox.vitalis - self.defect)
        elif self.defect_attribute.lower() == "max_health":
            mortanox.max_vitalis = max(1, mortanox.max_vitalis - self.defect)
            mortanox.vitalis = min(mortanox.vitalis, mortanox.max_vitalis)
        elif self.defect_attribute.lower() == "jump_height":
            mortanox.jump_height = max(5, mortanox.jump_height - self.defect)
        elif self.defect_attribute.lower() == "attack_speed":
            mortanox.attack_cooldown += (self.defect * 10)
        elif self.defect_attribute.lower() == "damage":
            mortanox.damage = max(1, mortanox.damage - self.defect)
    
    def apply(self, mortanox):
        assert type(mortanox) == Mortanox
        """Apply both positive and negative effects"""
        self.apply_positive(mortanox)
        if self.defect_attribute:
            self.apply_negative(mortanox)
    
    def buy(self, mortanox):
        assert type(mortanox) == Mortanox
        """Purchase the jar and apply its effects"""
        from assets import lucarii_collected, save_lucarii
        import assets
        
        if assets.lucarii_collected >= self.price:
            assets.lucarii_collected -= self.price
            if self.duration==-1:
                self.price *= 1.5
        else:
            return False
    def remove(self,mortanox):
        self.apply_positive(mortanox,-1)
    def remove_after_duration(self,fps,mortanox):
        self.used_duration+=1000//fps
        if self.used_duration>=self.duration:
            self.used_duration=0
            self.remove(mortanox)