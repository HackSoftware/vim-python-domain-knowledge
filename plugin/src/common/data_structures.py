from collections import namedtuple


Import = namedtuple("Import", ["module", "name", "alias", "is_relative"])
Export = namedtuple("Export", ["path", "name", "type"])
