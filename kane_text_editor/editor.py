
class Editor:
    buffer = []
    cursor = 0

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

    def append(self, c: str):
        self.buffer.insert(self.cursor, c)
        self.cursor += 1

    def delete(self):
        if len(self.buffer) > self.cursor:
            del self.buffer[self.cursor]

    def backspace(self):
        if self.buffer and self.cursor > 0:
            self.cursor -= 1
            self.delete()