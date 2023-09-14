import arcade
import arcade.gui


# --- Method 1 for handling click events,
# Create a child class.
class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class MenuMapWindow(arcade.Section):
    def __init__(self, left: int, bottom: int, width: int, height: int):
        super().__init__(left, bottom, width, height)
        self.v_box = arcade.gui.UIBoxLayout()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        for button_name in ["gui", "pizda"]:
            button_map = arcade.gui.UIFlatButton(text=button_name, width=200)
            self.v_box.add(button_map.with_space_around(bottom=20))

    def setup(self):
        pass
