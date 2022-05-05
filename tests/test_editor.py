#!/usr/bin/env python

"""Tests for `kane_text_editor` package."""

import pytest

from kane_text_editor import editor

def test_editor_starts_off_empty():
    e = editor.Editor()
    assert e.get() == ""
    assert e.cursor_position() == 0

def test_editor_starts_off_with_inital_string():
    e = editor.Editor("The quick brown fox")
    assert e.get() == "The quick brown fox"
    assert e.cursor_position() == 19

def test_editor_add_one_character():
    e = editor.Editor()
    e.append('x')
    assert e.get() == "x"
    assert e.cursor_position() == 1

def test_editor_add_two_characters():
    e = editor.Editor()
    e.append('x')
    e.append('y')
    assert e.get() == "xy"
    assert e.cursor_position() == 2

def test_editor_add_one_character_then_backspace():
    e = editor.Editor()
    e.append('x')
    e.backspace()
    assert e.get() == ""
    assert e.cursor_position() == 0

def test_editor_add_two_characters_then_backspace():
    e = editor.Editor()
    e.append('x')
    e.append('y')
    e.backspace()
    assert e.get() == "x"
    assert e.cursor_position() == 1

def test_editor_cursor_back():
    e = editor.Editor("The quick brown fox")
    e.cursor_backward()
    e.cursor_backward()
    assert e.cursor_position() == 17

def test_editor_cursor_forward():
    e = editor.Editor("The quick brown fox")
    e.cursor_forward()
    assert e.cursor_position() == 19
    e.cursor_backward()
    e.cursor_backward()
    e.cursor_forward()
    assert e.cursor_position() == 18

def test_editor_insert_character():
    e = editor.Editor("The quick brown fox")
    e.cursor_backward()
    e.cursor_backward()
    e.backspace()
    e.append('F')
    assert e.get() == "The quick brown Fox"

