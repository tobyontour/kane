#!/usr/bin/env python

"""Tests for `kane_text_editor` package."""

from kane_text_editor import editor


def test_editor_starts_off_empty():
    e = editor.Editor()
    assert str(e) == ""


def test_editor_starts_off_with_inital_string():
    e = editor.Editor("The quick brown fox")
    assert str(e) == "The quick brown fox"


def test_editor_with_simple_insertion():
    e = editor.Editor("The quick brown fox")
    e.move(5, 0)
    e.append("XXX")
    assert str(e) == "The qXXXuick brown fox"
    assert e.position() == (8, 0)


def test_editor_with_simple_editting():
    e = editor.Editor("The quick brown fox")
    e.cursor_backward()
    e.cursor_backward()
    e.cursor_forward()
    e.cursor_forward()
    e.cursor_forward()
    e.cursor_backward()
    e.backspace()
    assert e.position() == (1, 0)
    assert str(e) == "Te quick brown fox"


def test_editor_starts_off_with_inital_multiline_string():
    e = editor.Editor("""The quick brown fox
jumped over the lazy
dog's back.""")
    assert str(e) == """The quick brown fox
jumped over the lazy
dog's back."""


def test_editor_get_current_position_initial():
    e = editor.Editor("The quick brown fox")
    assert e.position() == (0, 0)


def test_editor_get_current_position_after_move():
    e = editor.Editor("""The quick brown fox
jumped over the lazy
dog's back.""")
    e.move(6, 1)
    assert e.position() == (6, 1)


def test_editor_get_current_position_after_move_off_end_of_text():
    e = editor.Editor("""The quick brown fox
jumped over the lazy
dog's back.""")
    e.move(20, 10)
    assert e.position() == (11, 2)


def test_editor_move_with_one_parameter_does_not_change_y():
    '''
    Not sure about this.
    '''
    e = editor.Editor("""The quick brown fox
jumped over the lazy
dog's back.""")
    e.move(6, 1)
    e.move(3)
    assert e.position() == (3, 1)


def test_editor_deals_with_added_multiple_line_return_from_line_editor():
    e = editor.Editor("""The quick brown fox
jumped over the lazy
dog's back.""")

    e.move(6, 1)
    e.append(" with\nease")

    assert e.position() == (4, 2)
    assert str(e) == """The quick brown fox
jumped with
ease over the lazy
dog's back."""


def test_editor_deals_with_added_line_return_from_line_editor():
    e = editor.Editor("""The quick brown fox""")
    e.append("\n")

    assert e.position() == (0, 1)
    assert str(e) == """
The quick brown fox"""


def test_editor_cursor_backwards_at_start_of_second_line():
    e = editor.Editor("""The quick brown fox\njumped over""")
    e.move(0, 1)
    e.cursor_backward()

    assert e.position() == (19, 0)
    assert str(e) == """The quick brown fox\njumped over"""


def test_editor_cursor_forwards_at_end_of_first_line():
    e = editor.Editor("""The quick brown fox\njumped over""")
    e.move(19, 0)
    e.cursor_forward()

    assert e.position() == (0, 1)
    assert str(e) == """The quick brown fox\njumped over"""


def test_editor_cursor_forwards_at_end_of_last_line():
    e = editor.Editor("""The quick brown fox\njumped over""")
    e.move(11, 1)
    e.cursor_forward()

    assert e.position() == (11, 1)
    assert str(e) == """The quick brown fox\njumped over"""


def test_editor_cursor_up():
    e = editor.Editor("""The quick brown fox\njumped over""")
    e.move(5, 1)
    e.cursor_up()

    assert e.position() == (5, 0)
    assert str(e) == """The quick brown fox\njumped over"""


def test_editor_cursor_up_to_a_shorter_line():
    e = editor.Editor("""The quick brown fox\njumped over the lazy dog's back""")
    e.move(25, 1)
    e.cursor_up()

    assert e.position() == (19, 0)
    assert str(e) == """The quick brown fox\njumped over the lazy dog's back"""


def test_editor_cursor_down():
    e = editor.Editor("""The quick brown fox\njumped over""")
    e.move(6, 0)
    e.cursor_down()

    assert e.position() == (6, 1)
    assert str(e) == """The quick brown fox\njumped over"""


def test_editor_cursor_down_off_end():
    e = editor.Editor("""The quick brown fox\njumped over""")
    e.move(16, 0)
    e.cursor_down()

    assert e.position() == (11, 1)
    assert str(e) == """The quick brown fox\njumped over"""


def test_editor_backspace_at_start_of_second_line():
    e = editor.Editor("""The quick brown fox\njumped over\nx""")
    e.move(0, 1)
    e.backspace()

    assert e.position() == (19, 0)
    assert str(e) == """The quick brown foxjumped over\nx"""


def test_editor_append_text_beyond_word_wrap():
    e = editor.Editor("""0123456789""")
    e.move(10, 0)
    e.set_word_wrap(10)
    e.append(" ")

    assert str(e) == """0123456789\n"""
    assert e.position() == (0, 1)


def test_editor_append_text_beyond_word_wrap_word_break():
    e = editor.Editor("""The quick brown fox jumped over.""")
    e.set_word_wrap(10)
    e.wrap()

    assert str(e) == """The quick\nbrown fox\njumped\nover."""


def test_editor_append_text_beyond_word_wrap_word_break_cursor_position():
    e = editor.Editor("""The quick\nbrown fox\njumped\nover.""")
    e.set_word_wrap(10)
    e.wrap()
    e.move(9, 1)
    e.append(" lazily ")

    assert str(e) == """The quick\nbrown fox\nlazily\njumped\nover."""
