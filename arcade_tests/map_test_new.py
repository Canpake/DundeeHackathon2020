import arcade
from final import country_info

SCREEN_WIDTH = 1186
SCREEN_HEIGHT = 609
SCREEN_TITLE = "Starting Template"


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        # If you have sprite lists, you should create them here, and set them to None

        # Additional attributes
        self.background = None  # background texture
        self.country = None     # country on mouseover
        self.flag_url = None    # country flag on mouseover

    def setup(self):
        # Create your sprites and sprite lists here
        self.background = arcade.load_texture("../images/world_map.png")

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        # background
        arcade.draw_xywh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # text
        arcade.draw_text(self.country, 20, 20, arcade.color.BLACK, 14)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        # converts x,y position on the screen into map coordinates, more or less
        def convert_coordinates(x, y):
            # latitude: 0:605 to -90:90
            lat = (y - 302)/302 * 90
            # longitude: 0:1186 to -180:180
            long = (x - 593)/593 * 180
            return lat, long

        # report on positions
        lat, long = convert_coordinates(x, y)   # a bit inaccurate but oh well

        # use latitude and longitude to get country + information
        self.country, facts, trends, self.flag_url = country_info.get_info(lat, long)
        print(self.country)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()