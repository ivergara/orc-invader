import random
import sys

import arcade

from __init__ import *
from entities import Player, Enemy, Arrow


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.ASH_GREY)

        self.frame_count = 0
        self.player_list = None
        self.plater_bullet_list = None
        self.enemy_list = None
        self.enemy_bullet_list = None

        self.player = None
        self.score = 0

        self.current_state = STATUS_RUNNING

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

        for i in range(ENEMY_COUNT):
            enemy = Enemy("../images/down_stand.png", SPRITE_SCALING_ENEMY)

            enemy.center_x = i*SCREEN_WIDTH/10+20
            enemy.center_y = SCREEN_HEIGHT*9/10

            self.enemy_list.append(enemy)

        self.player = Player()
        self.player_list.append(self.player)
    
    def draw_game_over(self):
        output = "Game Over"
        arcade.draw_text(output, SCREEN_WIDTH/2., SCREEN_HEIGHT/2., arcade.color.RED, 54, align="center",
                         anchor_x="center", anchor_y="center")

    def draw_game(self):
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()
        self.player_list.draw()
        self.player_bullet_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_draw(self):
        arcade.start_render()

        self.draw_game()

        if self.current_state == STATUS_PAUSE:
            arcade.draw_text("Paused!", SCREEN_WIDTH/2., SCREEN_HEIGHT/2., arcade.color.WHITE, 54, align="center",
                         anchor_x="center", anchor_y="center")
        elif self.current_state == STATUS_RUNNING:
            self.draw_game()
        elif self.current_state == STATUS_GAME_OVER:
            self.draw_game()
            self.draw_game_over()

    def update(self, delta_time):

        if self.current_state == STATUS_RUNNING:
            self.player.update()
            self.enemy_list.update()

            hit_list = arcade.check_for_collision_with_list(self.player,
                                                            self.enemy_list)

            if hit_list:
                self.current_state = STATUS_GAME_OVER

            self.enemy_bullet_list.update()
            self.player_bullet_list.update()

            for enemy in self.enemy_list:

                if random.randrange(200) == 0:
                    bullet = arcade.Sprite("../images/arrow.png", 0.20)
                    bullet.center_x = enemy.center_x
                    bullet.rotate = 180
                    bullet.top = enemy.bottom
                    bullet.change_y = -2
                    self.enemy_bullet_list.append(bullet)

                if enemy.top < 0:
                    self.current_state = STATUS_GAME_OVER

            for bullet in self.player_bullet_list:

                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

                if len(hit_list) > 0:
                    bullet.kill()

                for enemy in hit_list:
                    enemy.kill()
                    self.score += 1

                    # arcade.sound.play_sound(self.hit_sound)

                if bullet.bottom > SCREEN_HEIGHT:
                    bullet.kill()

            for bullet in self.enemy_bullet_list:

                hit_list = arcade.check_for_collision_with_list(bullet, self.player_list)

                if hit_list:
                    self.current_state = STATUS_GAME_OVER

                # arcade.sound.play_sound(self.hit_sound)

                if bullet.top < 0:
                    bullet.kill()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            bullet = Arrow("../images/arrow.png", 0.15, self.player)
            self.bullet_list.append(bullet)
        elif key == arcade.key.P:
            self.toggle_pause()
        elif key == arcade.key.Q:
            sys.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def toggle_pause(self):
        if self.current_state == STATUS_PAUSE:
            arcade.start_render()
            self.current_state = STATUS_RUNNING
        else:
            arcade.finish_render()
            self.current_state = STATUS_PAUSE


def main():
    window = MyGame(640, 480, "Orc-Invader Python")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
