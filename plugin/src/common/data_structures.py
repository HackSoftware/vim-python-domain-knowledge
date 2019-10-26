from collections import namedtuple


Import = namedtuple('Import', ['module', 'name', 'alias', 'is_relative'])
Class = namedtuple('Class', ['file_path', 'name', 'parents', 'module'])
Function = namedtuple('Function', ['file_path', 'name', 'module', 'arguments'])
