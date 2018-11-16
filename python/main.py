import random

import arcade

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MOVEMENT_SPEED = 3

SPRITE_SCALING_ENEMY = 1.2
ENEMY_COUNT = 10


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        # self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1


class Enemy(arcade.Sprite):
    """
    This class represents the enemy on our screen.
    """

    # def reset_pos(self):

    #     # Reset the coin to a random spot above the screen
    #     self.center_y = random.randrange(SCREEN_HEIGHT + 20,
    #                                      SCREEN_HEIGHT + 100)
    #     self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        # Move the coin
        self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, game over
        if self.top < 0:
            arcade.draw_text("Game Over", SCREEN_HEIGHT/2, SCREEN_WIDTH/2, arcade.color.WHITE, 14)


class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        # file_path = os.path.dirname(os.path.abspath(__file__))
        # os.chdir(file_path)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.ASH_GREY)

        self.frame_count = 0
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None

        self.player = None

        # Create our player
        # self.player = Player(SCREEN_WIDTH/2., 0, 15, arcade.color.AUBURN)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Create the coins
        for i in range(ENEMY_COUNT):
            enemy = Enemy("../images/down_stand.png", SPRITE_SCALING_ENEMY)

            # Position the enemy
            enemy.center_x = i*SCREEN_WIDTH/10+20
            enemy.center_y = SCREEN_HEIGHT*9/10

            self.enemy_list.append(enemy)

        # Add player ship
        self.player = Player("../images/up_stand.png", 1)
        self.player.center_x = SCREEN_WIDTH/2.
        self.player.center_y = SCREEN_HEIGHT/10.
        self.player_list.append(self.player)

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

    def update(self, delta_time):
        self.player.update()
        self.enemy_list.update()

        hit_list = arcade.check_for_collision_with_list(self.player,
                                                        self.enemy_list)

        if hit_list:
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.WHITE, 54)

        self.bullet_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.kill()

            # For every coin we hit, add to the score and remove the coin
            for enemy in hit_list:
                enemy.kill()
                # self.score += 1

                # # Hit Sound
                # arcade.sound.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.kill()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            bullet = arcade.Sprite("../images/arrow.png", 0.15)
            bullet.change_y = 1.5
            # Position the bullet
            bullet.center_x = self.player.center_x
            bullet.bottom = self.player.top

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0


def main():
    window = MyGame(640, 480, "Orc-Invader Python")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()