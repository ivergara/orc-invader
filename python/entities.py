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

    def shoot(self):
        return Arrow("../images/arrow.png", 0.15, self)


class Enemy(arcade.Sprite):
    def update(self):
        self.center_y -= 0.8

    def shoot(self):
        bullet = None
        """Shooting strategy for enemies."""
        if random.randrange(300) == 0:
            bullet = Arrow("../images/arrow.png", 0.20, self)
            bullet.rotate = 180
            bullet.top = self.bottom
            bullet.change_y = -2
            # bullet_list.append(bullet)
        return bullet


class Enemies():
    @classmethod
    def setup(cls, enemy_count):
        enemy_list = arcade.SpriteList()
        for i in range(enemy_count):
            enemy = Enemy("../images/down_stand.png", SPRITE_SCALING_ENEMY)

            enemy.center_x = i*SCREEN_WIDTH/10+20
            enemy.center_y = SCREEN_HEIGHT*9/10

            enemy_list.append(enemy)
        return enemy_list


class Arrow(arcade.Sprite):
    def __init__(self, filename, scale, origin):
        """An arrow requires an entity of origin, another arcade.Sprite
        instance."""
        super().__init__(filename, scale)

        self.change_y = 1.5
        self.center_x = origin.center_x
        self.bottom = origin.top
