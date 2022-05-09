"""Main module."""

from rich.panel import Panel
from textual.reactive import Reactive
from textual.widget import Widget
from editor import Editor
from datetime import datetime

class KaneTextEditor(Widget):
    buffer_change = Reactive(False)
    ed = Editor("The quick brown fox")

    def __init__(self, name: str = None) -> None:
        super().__init__(name)

    def render(self) -> Panel:
        return Panel(self.ed.get() + str(datetime.now()))

    def on_key(self, event):
        psadsdfrint("X")
        if event.key.isprintable():
            self.ed.append(event.key)
            self.buffer_change = not self.buffer_change

if __name__ == "__main__":
    from textual.app import App

    class EditorApp(App):

        async def on_mount(self) -> None:
            await self.view.dock(KaneTextEditor())

    EditorApp.run(log="textual.log")