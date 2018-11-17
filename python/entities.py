import random

import arcade

from __init__ import *


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("../images/up_stand.png", 1)

        self.center_x = SCREEN_WIDTH/2.
        self.center_y = SCREEN_HEIGHT/10.

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

    def shoot(self, bullet_list):
        """Shooting strategy for enemies."""
        if random.randrange(200) == 0:
            bullet = Arrow("../images/arrow.png", 0.20, self)
            bullet.rotate = 180
            bullet.top = self.bottom
            bullet.change_y = -2
            bullet_list.append(bullet)


class Arrow(arcade.Sprite):
    def __init__(self, filename, scale, origin):
        """An arrow requires an entity of origin, another arcade.Sprite
        instance."""
        super().__init__(filename, scale)

        self.change_y = 1.5
        self.center_x = origin.center_x
        self.bottom = origin.top
