from enum import Enum


class WrapType(Enum):
    NONE = 0
    CHARACTER = 1
    WORD = 2


class Editor:
    lines = []
    current_line = None
    current_line_editor = None
    wrap_length = None
    wrap_type = WrapType.NONE

    def __init__(self, s: str = "") -> None:
        self.lines = s.splitlines()
        if not self.lines:
            self.lines = [""]
        self.current_line = 0
        self.current_line_editor = LineEditor(self.lines[0])
        self.current_line_editor.cursor_move(0)

    def set_word_wrap(self, wr: int) -> None:
        self.wrap_type = WrapType.WORD
        self.wrap_length = wr

    def set_character_wrap(self, wr: int) -> None:
        self.wrap_type = WrapType.CHARACTER
        self.wrap_length = wr

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

    def is_cursor_at_end_of_line(self):
        return self.current_line_editor.cursor_position() \
                == len(self.lines[self.current_line])

    def cursor_forward(self):
        if self.is_cursor_at_end_of_line() \
                and self.current_line != len(self.lines) - 1:
            self.move(0, self.current_line + 1)
        else:
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
        if self.current_line_editor.cursor_position() == 0:
            if self.current_line == 0:
                return
            else:
                final_x = len(self.lines[self.current_line - 1])
                self.move(final_x, self.current_line - 1)
                tmp = self.lines.pop(self.current_line + 1)
                self.append(tmp)
                self.move(final_x)
        else:
            self.current_line_editor.backspace()
        self.update()

    def append(self, data: str):
        self.current_line_editor.append(data)
        self.update()
        self.wrap()

        # Now update the cursor
        data_lines = data.split('\n')
        if len(data_lines) != 1:
            self.move(len(data_lines[-1]),
                      self.current_line + len(data_lines) - 1)

    def wrap(self):
        if self.wrap_length is None or self.wrap_type == WrapType.NONE:
            return

        if self.wrap_type == WrapType.CHARACTER:
            pass
        elif self.wrap_type == WrapType.WORD:
            self.word_wrap()

    def word_wrap(self):
        start = 0
        y = self.current_line
        for i, line in enumerate(self.lines, start):
            if len(line) > self.wrap_length:
                if i >= len(self.lines) - 1:
                    self.lines.append("")

                split_point = self.wrap_length
                # If there's a space in the line before the word wrap we can
                # split on.
                if line.rfind(' ', 0, self.wrap_length) != -1:
                    split_point = line.rfind(' ', 0, self.wrap_length) + 1
                elif len(line) == (self.wrap_length + 1) and line[-1] == ' ':
                    line = line[:-1]

                if len(self.lines[i + 1]) > 0:
                    if self.lines[i + 1][0] == ' ':
                        self.lines[i + 1] = line[split_point:] + self.lines[i + 1]
                    else:
                        self.lines[i + 1] = line[split_point:] + ' ' + self.lines[i + 1]
                else:
                    self.lines[i + 1] = line[split_point:]
                if i == y:
                    y += 1

                self.lines[i] = line[0:split_point].rstrip()

        self.move(self.position()[0], y)


    def update(self):
        line_editor_content = self.current_line_editor.get().splitlines()
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
