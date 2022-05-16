#!/usr/bin/env python

"""Tests for `kane_text_editor` package."""

import pytest

from kane_text_editor import editor

def test_editor_starts_off_empty():
    e = editor.Editor()
    assert e.get() == ""

def test_editor_starts_off_with_inital_string():
    e = editor.Editor("The quick brown fox")
    assert e.get() == "The quick brown fox"

def test_editor_starts_off_with_inital_multiline_string():
    e = editor.Editor("""The quick brown fox
jumped over the lazy
dog's back.""")
    assert e.get() == """The quick brown fox
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
    assert e.position() == (10, 2)

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