import os
import ast
from collections import namedtuple

from ..settings import CURRENT_DIRECTORY


Import = namedtuple("Import", ["module", "name", "alias"])
Export = namedtuple("Export", ["path", "name", "type"])


def find_all_files():
    result = []

    for root, _, files in os.walk(CURRENT_DIRECTORY):
        python_files = [
            (os.path.join(root, file))
            for file in files
            if file.endswith('.py')
        ]
        result.extend(python_files)

    return result


def get_imports_from_file(path):
    with open(path, 'r') as file:
        root = ast.parse(file.read(), path)

    for node in ast.iter_child_nodes(root):
        is_import = isinstance(node, ast.Import)
        is_import_from = isinstance(node, ast.ImportFrom)

        if not (is_import or is_import_from):
            continue

        if is_import:
            module = []

        if is_import_from:
            module = ''
            if node.module:
                module = node.module.split('.')

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname)


def get_exports_from_file(path):
    with open(path, 'r') as file:
        root = ast.parse(file.read(), path)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.FunctionDef):
            yield Export(
                path,
                node.name,
                'function'
            )

        if isinstance(node, ast.ClassDef):
            yield Export(
                path,
                node.name,
                'class'
            )


def find_proper_line_for_import(buffer, module_name):
    # TODO: Rework this ? :(
    for line_number, line in enumerate(buffer):
        if module_name in line:
            return line_number

    return 0


def get_imports_from_files(paths):
    for path in paths:
        yield from get_imports_from_file(path)


def get_exports_from_files(paths):
    for path in paths:
        yield from get_exports_from_file(path)


def is_import_in_file(*, import_statement, vim_buffer):
    return any(
        [
            bool(import_statement in line)
            for line in vim_buffer
        ]
    )
