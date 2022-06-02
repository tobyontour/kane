

class WordWrap:
    def __init__(self, wrap_length: int = 80) -> None:
        self.wrap_length = wrap_length

    def wrap_line(self, line: str) -> list:
        output = []
        if len(line) > self.wrap_length:
            space_left = self.wrap_length

            current_line = ''
            for word in line.split():
                if len(word) + 1 > space_left:
                    output.append(current_line)
                    space_left = self.wrap_length - len(word)
                else:
                    space_left = space_left - (len(word) + 1)
                    current_line = current_line + ' '
                current_line = current_line + word
        else:
            current_line = line

        output.append(current_line)
        return output

