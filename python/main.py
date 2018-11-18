import sys
from enum import Enum, auto

import arcade
from __init__ import *
from entities import Arrow, Enemies, Enemy, Player


class GameState(Enum):
    RUNNING = auto()
    PAUSED = auto()
    FINISHED = auto()
    GAME_OVER = auto()

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class OrcInvader(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.ASH_GREY)

        self.frame_count = 0
        self.player_list = None
        self.player_bullet_list = None
        self.enemy_list = None
        self.enemy_bullet_list = None

        self.player = None
        self.score = 0

        self.current_state = GameState.RUNNING

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_list = Enemies.setup(ENEMY_COUNT)
        self.enemy_bullet_list = arcade.SpriteList()

        self.player = Player()
        self.player_list.append(self.player)

    def draw_game_over(self):
        output = "Game Over"
        arcade.draw_text(output, SCREEN_WIDTH/2., SCREEN_HEIGHT/2., arcade.color.RED, 54, align="center",
                         anchor_x="center", anchor_y="center")

    def draw_finish(self):
        output = "You won!"
        arcade.draw_text(output, SCREEN_WIDTH/2., SCREEN_HEIGHT/2., arcade.color.GREEN, 54, align="center",
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

        if self.current_state == GameState.PAUSED:
            arcade.draw_text("Paused!", SCREEN_WIDTH/2., SCREEN_HEIGHT/2., arcade.color.WHITE, 54, align="center",
                         anchor_x="center", anchor_y="center")
        elif self.current_state == GameState.RUNNING:
            self.draw_game()
        elif self.current_state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.current_state == GameState.FINISHED:
            self.draw_game()
            self.draw_finish()

    def update(self, delta_time):

        if self.current_state == GameState.RUNNING:
            self.player.update()
            self.enemy_list.update()

            hit_list = arcade.check_for_collision_with_list(self.player,
                                                            self.enemy_list)

            if hit_list:
                self.current_state = GameState.GAME_OVER

            self.enemy_bullet_list.update()
            self.player_bullet_list.update()

            if not self.enemy_list:
                self.current_state = GameState.FINISHED

            for enemy in self.enemy_list:
                # use assignment expression once 3.8 is released
                bullet = enemy.shoot()
                if bullet:
                    self.enemy_bullet_list.append(bullet)

                if enemy.top < 0:
                    self.current_state = GameState.GAME_OVER

            for bullet in self.player_bullet_list:

                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

                if len(hit_list) > 0:
                    bullet.kill()

                for enemy in hit_list:
                    enemy.kill()
                    self.score += 1

                if bullet.bottom > SCREEN_HEIGHT:
                    bullet.kill()

            for bullet in self.enemy_bullet_list:

                hit_list = arcade.check_for_collision_with_list(bullet, self.player_list)

                if hit_list:
                    self.current_state =  GameState.PAUSED

                if bullet.top < 0:
                    bullet.kill()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            self.player_bullet_list.append(self.player.shoot())
        elif key == arcade.key.P:
            self.toggle_pause()
        elif key == arcade.key.Q:
            sys.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def toggle_pause(self):
        if self.current_state == GameState.PAUSED:
            arcade.start_render()
            self.current_state = GameState.RUNNING
        else:
            arcade.finish_render()
            self.current_state = GameState.PAUSED


def main():
    window = OrcInvader(640, 480, "Orc-Invader Python")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
