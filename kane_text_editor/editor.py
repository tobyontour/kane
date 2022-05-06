
from turtle import pos


class Editor:
    buffer = []
    cursor = 0
    clipboard_buffer = ""

    def __init__(self, s: str = "") -> None:
        self.buffer = list(s)
        self.cursor = len(s)

    def get(self):
        string = ""
        return string.join(self.buffer)

    def cursor_position(self):
        return self.cursor

    def cursor_backward(self):
        if self.cursor > 1:
            self.cursor -= 1

    def cursor_forward(self):
        if self.cursor < len(self.buffer):
            self.cursor += 1

    def cursor_move(self, position: int):
        if position < len(self.buffer) and position >= 0:
            self.cursor = position
        elif position >= len(self.buffer):
            self.cursor = len(self.buffer)
        else:
            self.cursor = 0

    def copy(self):
        if self.cursor < len(self.buffer):
            self.clipboard_buffer = self.buffer[self.cursor]

    def clipboard(self):
        return self.clipboard_buffer

    def append(self, data: str):
        for char in data:
            self.buffer.insert(self.cursor, char)
            self.cursor += 1

    def delete(self):
        if len(self.buffer) > self.cursor:
            self.clipboard_buffer = self.buffer[self.cursor]
            del self.buffer[self.cursor]

    def backspace(self):
        if self.buffer and self.cursor > 0:
            self.cursor -= 1
            self.delete()