import random
import math


class ScreenEffects:
    def __init__(self):
        self.recoil_offset_x = 0
        self.recoil_offset_y = 0
        self.shake_duration = 0
        self.recoil_decay = 0.95
        self.shake_intensity = 2

    def recoil(self, angle, recoil_strength=3):
        self.recoil_offset_x = recoil_strength * math.cos(angle)
        self.recoil_offset_y = recoil_strength * math.sin(angle)
        self.shake_duration = self.shake_duration

    def update_recoil(self, player):
        if self.shake_duration > 0:
            player.rect.x -= int(self.recoil_offset_x)
            player.rect.y -= int(self.recoil_offset_y)

            self.recoil_offset_x *= self.recoil_decay
            self.recoil_offset_y *= self.recoil_decay

            self.shake_duration -= 1

    def screenshake(self, window=False):
        if self.shake_duration > 0:
            if window:
                self.shake_duration -= 1
                return (random.uniform(-self.shake_intensity-3, self.shake_intensity+3), 
                        random.uniform(-self.shake_intensity-3, self.shake_intensity+3))
            else:
                self.shake_duration -= 1
                return (random.uniform(-self.shake_intensity, self.shake_intensity), 
                        random.uniform(-self.shake_intensity, self.shake_intensity))
        else:
            return (0, 0)