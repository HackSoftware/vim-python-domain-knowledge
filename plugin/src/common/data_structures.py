from collections import namedtuple


Import = namedtuple('Import', ['module', 'name', 'alias', 'is_relative'])
Export = namedtuple('Export', ['path', 'name', 'type'])
Class = namedtuple('Class', ['file_path', 'name', 'parents'])
Function = namedtuple('Function', ['file_path', 'name'])
