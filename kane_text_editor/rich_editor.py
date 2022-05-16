
from editor import Editor

class RichEditor(Editor):

    def get_plain(self):
        return super().get()

    def get(self):
        backup = self.lines[self.current_line]
        if self.current_line_editor.cursor_position() < len(self.lines[self.current_line]):
            self.lines[self.current_line] = \
                backup[:self.current_line_editor.cursor_position()] + \
                "[reverse]" + \
                backup[self.current_line_editor.cursor_position()] + \
                "[/reverse]" + \
                backup[self.current_line_editor.cursor_position() + 1:]
        else:
            self.lines[self.current_line] = backup + "[reverse] [/reverse]"
        tmp = super().get()
        self.lines[self.current_line] = backup
        return tmp

