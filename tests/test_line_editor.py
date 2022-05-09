#!/usr/bin/env python

"""Tests for `kane_text_editor` package."""

import pytest

from kane_text_editor import editor

def test_editor_starts_off_empty():
    e = editor.LineEditor()
    assert e.get() == ""
    assert e.cursor_position() == 0

def test_editor_starts_off_with_inital_string():
    e = editor.LineEditor("The quick brown fox")
    assert e.get() == "The quick brown fox"
    assert e.cursor_position() == 19

def test_editor_add_one_character():
    e = editor.LineEditor()
    e.append('x')
    assert e.get() == "x"
    assert e.cursor_position() == 1

def test_editor_add_two_characters():
    e = editor.LineEditor()
    e.append('x')
    e.append('y')
    assert e.get() == "xy"
    assert e.cursor_position() == 2

def test_editor_add_one_character_then_backspace():
    e = editor.LineEditor()
    e.append('x')
    e.backspace()
    assert e.get() == ""
    assert e.cursor_position() == 0

def test_editor_add_two_characters_then_backspace():
    e = editor.LineEditor()
    e.append('x')
    e.append('y')
    e.backspace()
    assert e.get() == "x"
    assert e.cursor_position() == 1
    assert e.clipboard() == "y"

def test_editor_cursor_back():
    e = editor.LineEditor("The quick brown fox")
    e.cursor_backward()
    e.cursor_backward()
    assert e.cursor_position() == 17

def test_editor_cursor_forward():
    e = editor.LineEditor("The quick brown fox")
    e.cursor_forward()
    assert e.cursor_position() == 19
    e.cursor_backward()
    e.cursor_backward()
    e.cursor_forward()
    assert e.cursor_position() == 18

def test_editor_insert_character():
    e = editor.LineEditor("The quick brown fox")
    e.cursor_backward()
    e.cursor_backward()
    e.backspace()
    e.append('F')
    assert e.get() == "The quick brown Fox"
    assert e.cursor_position() == 17

def test_editor_insert_string():
    e = editor.LineEditor("The quick brown fox")
    e.backspace()
    e.backspace()
    e.backspace()
    e.append('cat')
    assert e.get() == "The quick brown cat"
    assert e.cursor_position() == 19

def test_editor_move_cursor():
    e = editor.LineEditor("The quick brown fox")
    e.cursor_move(4)
    e.append('very ')
    assert e.get() == "The very quick brown fox"
    assert e.cursor_position() == 9

def test_editor_move_cursor_off_end():
    e = editor.LineEditor("The quick brown fox")
    e.cursor_move(40)
    e.append('very ')
    assert e.get() == "The quick brown foxvery "
    assert e.cursor_position() == 24

def test_editor_move_cursor_off_start():
    e = editor.LineEditor("The quick brown fox")
    e.cursor_move(-5)
    assert e.cursor_position() == 0
    e.append('very ')
    assert e.get() == "very The quick brown fox"
    assert e.cursor_position() == 5

def test_editor_copy_character():
    e = editor.LineEditor("The quick brown fox")
    e.cursor_move(4)
    e.copy()
    assert e.cursor_position() == 4
    e.cursor_move(0)
    assert e.clipboard() == 'q'
    e.append(e.clipboard())
    assert e.get() == "qThe quick brown fox"
    assert e.cursor_position() == 1
