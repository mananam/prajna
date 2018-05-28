# -*- coding: utf-8 -*-
"""Prajna - tools for sanskrit translation."""
import logging

from collections import namedtuple
from bs4 import BeautifulSoup
from stargaze import Dictionary
from sanskrit_parser.base.sanskrit_base import SanskritObject

logger = logging.getLogger("prajna")
DictionaryEntry = namedtuple("DictionaryEntry", "word meaning grammar")


class EnglishTranslator(object):
    """Sanskrit to English translation engine."""

    def __init__(self, dicts, slp1=True):
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

        parser = DictParser("spokensanskrit")
        definitions = []
        for w in text.split(' '):
            word = SanskritObject(w)
            for dic in self._dicts:
                defn = parser.parse(dic.lookup(word.devanagari()))
                if len(defn) > 0:
                    definitions.append(defn[0])
                    logger.debug("{}: {}".format(word.canonical(), defn[0]))

        return definitions[0] if len(definitions) > 0 else None


class DictParser(object):
    """Parser for dictionary definitions."""

    def __init__(self, dictname):
        """Create a DictParser instance."""
        if dictname == "spokensanskrit":
            self._parser = self._parse_spokensanskrit
        else:
            logger.debug("No matching parser available.")

    def parse(self, text):
        """Parse dictionary definition text to objects."""
        if self._parser is not None:
            return self._parser(text)
        return []

    def _parse_spokensanskrit(self, text):
        defs = []
        if text is None:
            return defs
        soup = BeautifulSoup(text, 'html.parser')
        for entry in soup.table.find_all("tr"):
            columns = entry.find_all("td")
            defs.append(DictionaryEntry(word=columns[1].get_text(),
                                        meaning=columns[4].get_text(" "),
                                        grammar=columns[3].get_text(" ")))
        return defs
