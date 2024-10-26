# type: ignore
"""
My first application.
"""
import toga
from toga import Box, Button, InfoDialog, Label
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.window import MainWindow


class HelloWorld(toga.App):
    def startup(self) -> None:
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = Label(
            "Your name: ",
            style=Pack(padding=(0, 5)),
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = Button(
            "Say Hello!",
            on_press=self.say_hello,
            style=Pack(padding=5),
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = MainWindow(title=self.formal_name)
        assert isinstance(self.main_window, MainWindow)
        self.main_window.content = main_box
        self.main_window.show()

    async def say_hello(self, widget: Button) -> None:
        assert isinstance(widget, Button)
        await self.main_window.dialog(InfoDialog(greeting(self.name_input.value), "Hi there!"))


def greeting(name: str) -> str:
    if name:
        return f"Hello, {name}"
    return "Hello, stranger"


def main() -> HelloWorld:
    return HelloWorld()
