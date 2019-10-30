from collections import namedtuple


Import = namedtuple('Import', ['id', 'module', 'name', 'alias', 'is_relative'])
Class = namedtuple('Class', ['id', 'file_path', 'name', 'parents', 'module'])
Function = namedtuple('Function', ['id', 'file_path', 'name', 'module', 'arguments'])
