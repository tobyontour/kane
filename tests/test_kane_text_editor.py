#!/usr/bin/env python

"""Tests for `kane_text_editor` package."""

import pytest


from kane_text_editor import kane_text_editor, editor


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

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
