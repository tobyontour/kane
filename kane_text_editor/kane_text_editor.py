"""Main module."""

from xmlrpc.client import boolean
from rich.panel import Panel
from textual.reactive import Reactive
from textual.widget import Widget
import textual
from rich_editor import RichEditor


class KaneTextEditor(Widget):
    buffer_change = Reactive(False)
    ed = RichEditor("The quick brown fox jumped over. ")

    def __init__(self, name: str = None) -> None:
        super().__init__(name)

    def render(self) -> Panel:
        return Panel(self.ed.get())

    def on_key(self, event: textual.events.Key) -> None:
        if self.process_key(event.key):
            if self.buffer_change:
                self.buffer_change = False
            else:
                self.buffer_change = True

    def process_key(self, key: str) -> boolean:
        update_required = True
        if key.isprintable() and len(key) == 1:
            self.ed.append(key)
        elif key == 'enter':
            self.ed.append("\n")
        elif key == 'left':
            self.ed.cursor_backward()
        elif key == 'right':
            self.ed.cursor_forward()
        elif key == 'up':
            self.ed.cursor_up()
        elif key == 'down':
            self.ed.cursor_down()
        elif key == 'ctrl+h':
            self.ed.backspace()
        elif key == 'ctrl+w':
            self.ed.wrap()
        return update_required


if __name__ == "__main__":
    from textual.app import App

    class EditorApp(App):

        async def on_mount(self) -> None:
            self.kte = KaneTextEditor()
            self.kte.ed.move(0, 1)
            self.kte.ed.set_word_wrap(10)
            await self.view.dock(self.kte)

        async def on_key(self, event: textual.events.Key) -> None:
            self.kte.on_key(event)

    EditorApp.run(title="Editor test app", log="textual.log")
