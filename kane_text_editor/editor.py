
class Editor:
    lines = []
    current_line = None
    current_line_editor = None

    def __init__(self, s: str = "") -> None:
        self.lines = s.splitlines()
        if not self.lines:
            self.lines = [""]
        self.current_line = 0
        self.current_line_editor = LineEditor(self.lines[0])
        self.current_line_editor.cursor_move(0)

    def get(self):
        return "\n".join(self.lines)

    def position(self):
        if self.current_line_editor is not None:
            return (self.current_line_editor.cursor_position(),
                    self.current_line)

    def move(self, x: int, y: int = None):
        if y is None:
            y = self.current_line
        y = max(0, y)
        y = min(len(self.lines) - 1, y)
        x = max(0, x)
        x = min(len(self.lines[y]) + 1, x)

        if y != self.current_line or self.current_line_editor is None:
            self.current_line_editor = LineEditor(self.lines[y])

        self.current_line_editor.cursor_move(x)
        self.current_line = y

    def cursor_forward(self):
        self.current_line_editor.cursor_forward()
        self.update()

    def cursor_backward(self):
        if self.current_line_editor.cursor_position() == 0 and \
                self.current_line > 0:
            self.move(
                len(self.lines[self.current_line - 1]) + 1,
                self.current_line - 1)
        else:
            self.current_line_editor.cursor_backward()
        self.update()

    def cursor_up(self):
        self.move(self.current_line_editor.cursor, self.current_line - 1)
        self.update()

    def cursor_down(self):
        self.move(self.current_line_editor.cursor, self.current_line + 1)
        self.update()

    def backspace(self):
        self.current_line_editor.backspace()
        self.update()

    def append(self, data: str):
        self.current_line_editor.append(data)
        self.update()
        data_line_count = data.count('\n')
        if data_line_count > 0:
            data_lines = data.splitlines()
            self.move(len(data_lines[-1]), self.current_line + data_line_count)

    def update(self):
        line_editor_content = self.current_line_editor.get().splitlines()
        if self.current_line_editor.get()[-1][-1] == '\n':
           line_editor_content.append('')
        if len(line_editor_content) == 1:
            self.lines[self.current_line] = self.current_line_editor.get()
        elif self.current_line == 0:
            self.lines = line_editor_content + self.lines[1:]
        else:
            self.lines = self.lines[0:self.current_line] + \
                        line_editor_content + \
                        self.lines[self.current_line + 1:]


class LineEditor:
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
        if self.cursor > 0:
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
