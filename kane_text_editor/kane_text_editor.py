"""Main module."""

from rich.panel import Panel
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import ScrollView
import textual
from editor import Editor
from editor import LineEditor
from datetime import datetime

class KaneTextEditor(Widget):
    buffer_change = Reactive(False)
    ed = Editor("The quick brown fox")

    def __init__(self, name: str = None) -> None:
        super().__init__(name)

    def render(self) -> Panel:
        return Panel(self.ed.get())

    def on_key(self, event: textual.events.Key) -> None:
        if event.key.isprintable() and len(event.key) == 1:
            self.ed.append(event.key)
            if self.buffer_change:
                self.buffer_change = False
            else:
                self.buffer_change = True
        elif event.key == 'left':
            self.ed.cursor_backward()
        elif event.key == 'right':
            self.ed.cursor_forward()

if __name__ == "__main__":
    from textual.app import App

    class EditorApp(App):

        async def on_mount(self) -> None:
            self.kte = KaneTextEditor()
            await self.view.dock(self.kte)

        async def on_key(self, event: textual.events.Key) -> None:
            self.kte.on_key(event)

    EditorApp.run(title="Editor test app", log="textual.log")