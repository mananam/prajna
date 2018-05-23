# -*- coding: utf-8 -*-
"""Prajna - tools for sanskrit translation."""
import logging

from stargaze import Dictionary
from sanskrit_parser.base.sanskrit_base import SanskritObject

logger = logging.getLogger("prajna")


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

        # Analyze the input text
        # sanskrit_text = SanskritObject(text)

        definitions = []
        for w in text.split(' '):
            for dic in self._dicts:
                defn = dic.lookup(w)
                definitions.append(defn)
                logger.debug("{}: {}, ".format(SanskritObject(w).canonical(), defn))

        return definitions[0] if len(definitions) > 0 else None
