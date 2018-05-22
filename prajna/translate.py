# -*- coding: utf-8 -*-
"""Prajna - tools for sanskrit translation."""
from stargaze import Dictionary


class EnglishTranslator(object):
    """Sanskrit to English translation engine."""

    def __init__(self, dicts):
        """Create an instance of the English Translator.

        Args:
            dicts (dict): dictionary of sanskrit-english dictionaries
        """
        self._dict_config = dicts
        self._dicts = []

    def translate(self, text):
        """Translate a source text in sanskrit to english."""
        if self._dicts == []:
            for k, v in self._dict_config.items():
                self._dicts.append(Dictionary(v))

        definitions = []
        for dic in self._dicts:
            definitions.append(dic.lookup(text))

        return definitions[0] if len(definitions) > 0 else None
