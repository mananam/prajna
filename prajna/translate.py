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

    def __init__(self, dicts, slp1=False):
        """Create an instance of the English Translator.

        Args:
            dicts (dict): dictionary of sanskrit-english dictionaries
        """
        self._dict_config = dicts
        self._dicts = []
        self._use_slp1 = slp1

    def translate(self, text):
        """Translate a source text in sanskrit to english."""
        if self._dicts == []:
            for k, v in self._dict_config.items():
                self._dicts.append(Dictionary(v))
                parser = DictParser(k)

        # Analyze the input text
        # sanskrit_text = SanskritObject(text)

        definitions = []
        for w in text.split(' '):
            if self._use_slp1:
                w = SanskritObject(w).devanagari()
            for dic in self._dicts:
                defn = parser.parse(dic.lookup(w))
                if len(defn) > 0:
                    definitions.append(defn[0])
                    logger.debug("{}: {}".format(SanskritObject(w).canonical(), defn[0]))

        return definitions[0].meaning if len(definitions) > 0 else None


class DictParser(object):
    """Parser for dictionary definitions."""

    def __init__(self, dictname):
        """Create a DictParser instance."""
        if dictname == "spokensanskrit":
            self._parser = self._parse_spokensanskrit
        else:
            self._parser = self._parse_generic
            logger.debug("No matching parser available. Using a generic parser.")

    def parse(self, text):
        """Parse dictionary definition text to objects."""
        return self._parser(text)

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

    def _parse_generic(self, text):
        # We don't have few data for a generic parser. Just return the meaning
        return [DictionaryEntry(word=None, meaning=text, grammar=None)]
