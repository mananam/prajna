# -*- coding: utf-8 -*-
"""Tests for english translator."""
from prajna.translate import EnglishTranslator


def test_translate_should_output_word_meaning():
    t = EnglishTranslator({})

    assert t.translate("dummy") is None
