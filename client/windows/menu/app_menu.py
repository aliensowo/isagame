import arcade
import arcade.gui
from client.windows.menu_maps import app_maps


class MenuView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        super().__init__()
        self.popup = app_maps.MenuMapWindow()(0, 0, 400, 300)
        self.section_manager.add_section(self.popup)
        self.ma


    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.AQUA)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        # button_map = arcade.gui.UIFlatButton(text="Map List", width=200)
        # self.v_box.add(button_map.with_space_around(bottom=20))
        # button_map.on_click = self.on_click_map

        # arcade.draw_text("Space Invaders", self.window.width / 2, self.window.height / 2,
        #                  arcade.color.WHITE, font_size=50, anchor_x="center")
        # arcade.draw_text("Click to Start", self.window.width / 2, self.window.height / 2 - 75,
        #                  arcade.color.WHITE, font_size=20, anchor_x="center")

    def setup(self):
        self.v_box = arcade.gui.UIBoxLayout()

    def on_click_map(self, event):
        """ If the user presses the mouse button, start the game. """
        my_game_view = app_maps.MenuMapWindow()
        my_game_view.setup()
        self.window.show_view(my_game_view)

    # def on_mouse_press(self, _x, _y, _button, _modifiers):
    #     """ If the user presses the mouse button, start the game. """
    #     my_game_view = app_platform.MyGame()
    #     my_game_view.setup()
    #     self.window.show_view(my_game_view)
