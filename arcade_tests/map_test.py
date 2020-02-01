import math
import random
import arcade
import os

# --- Constants ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Map Test"
SPRITE_SCALE_PLAYER = 0.15
SPRITE_SCALE_MAP = 0.35
SPRITE_SCALE_BOX = 0.2
SPRITE_SCALE_PROJECTILE_DOT = 0.01
PROJECTILE_DOT_FREQ = 10
GRAV_CONST = 100


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.map_list = None

        # Set up the player info
        self.player_sprite = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.map_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()

        # Set up map
        map = arcade.Sprite("../images/world_map.png", scale=SPRITE_SCALE_MAP)
        map.center_x = SCREEN_WIDTH/2
        map.center_y = SCREEN_HEIGHT/2
        map.collision_radius = 40

        self.map_list.append(map)

        # Set up the player
        self.player_sprite = arcade.Sprite("../images/pin.png", scale=SPRITE_SCALE_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """ Draw everything """
        self.draw_frame += 1

        arcade.start_render()
        self.player_list.draw()
        self.map_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):

        projectile = arcade.Sprite("../images/pin.png", scale=SPRITE_SCALE_BOX)
        projectile.center_x = x
        projectile.center_y = y
        self.projectile_list.append(projectile)


    def on_update(self, delta_time):
        """ Movement and game logic """

        # for map in self.map_list:



def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()