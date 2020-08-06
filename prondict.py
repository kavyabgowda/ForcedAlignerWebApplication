import logging
from collections import defaultdict
from .utilities import SIL, SP
import os
class PronDict(object):
    SILENT_PHONES = frozenset([SIL, SP])

    @staticmethod
    def pronify(source):
        for (i, line) in enumerate(source, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                (word, pron) = line.split(None, 1)
            except ValueError:
                logging.error("Formatting error in dictionary '{}' (ln. {}).".format(source.name, i))
                exit(1)
            yield (i, word, pron.split())

    def add(self, filename):
        filePath=os.getcwd()+'/'+filename
        with open(filePath, "r") as source:
            for (i, word, pron) in PronDict.pronify(source):
                for ph in pron:
                    if ph not in self.ps | self.SILENT_PHONES:
                        logging.error("Unknown phone '{}' in dictionary '{}' (ln. {}).".format(ph, filename, i))
                        exit(1)
                self.d[word].append(pron)


    def __init__(self, phoneset, filename=None):
        self.ps = phoneset
        self.d = defaultdict(list)
        if filename:
            self.add(filename)
        self.oov = set()

    def __getitem__(self, key):
        getlist = self.d[key]
        if getlist:
            return getlist
        else:
            self.oov.add(key)
            raise KeyError(key)


    def __contains__(self, key):
        return key in self.d and self.d[key] != []

    def __repr__(self):
        return "PronDict({})".format(self.d)

    def __setitem__(self, key, value):
        self.d[key].append(value)
