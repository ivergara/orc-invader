import arcade

from __init__ import *


class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x

        # hard boundaries
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1


class Enemy(arcade.Sprite):
    def update(self):
        self.center_y -= 1.5


class Arrow(arcade.Sprite):
    def __init__(self, filename, scale, origin):
        """An arrow requires an entity of origin, another arcade.Sprite
        instance."""
        super().__init__(filename, scale)

        self.change_y = 1.5
        self.center_x = origin.center_x
        self.bottom = origin.top
