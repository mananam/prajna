# -*- coding: utf-8 -*-
"""Tests for english translator."""
import prajna.translate


def test_translate_should_output_word_meaning():
    # TODO
    t = prajna.translate.EnglishTranslator({})

    assert t.translate("dummy") is None


def test_translate_should_output_word_meaning_slp1():
    # TODO
    t = prajna.translate.EnglishTranslator({}, slp1=True)

    assert t.translate("dummy") is None


def test_parser_should_return_empty_definition_for_invalid_text():
    p = prajna.translate.DictParser("spokensanskrit")

    defns = p.parse(None)

    assert defns == []


def test_parser_should_parse_generic_dictionary():
    p = prajna.translate.DictParser("unknown_dict")

    defns = p.parse("text")

    assert len(defns) == 1
    assert defns[0].word is None
    assert defns[0].meaning == "text"
    assert defns[0].grammar is None


def test_parser_should_parse_spokensanskrit():
    p = prajna.translate.DictParser("spokensanskrit")
    text = """<table><tr><td></td><td>word</td>
    <td>word_transliteration</td>
    <td><span style=color:#333>adj. ind.</span></td>
    <td><span style=color:#666>text defn</span></td>
    </tr></table>
    """

    defns = p.parse(text)

    assert len(defns) == 1
    assert defns[0].word == "word"
    assert defns[0].meaning == "text defn"
    assert defns[0].grammar == "adj. ind."
