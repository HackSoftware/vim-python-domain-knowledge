from collections import namedtuple


Import = namedtuple("Import", ["module", "name", "alias"])
Export = namedtuple("Export", ["path", "name", "type"])
