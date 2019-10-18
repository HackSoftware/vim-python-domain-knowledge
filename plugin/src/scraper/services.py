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


def _get_ast_from_file(file_content):
    try:
        return ast.parse(file_content)
    except:
        return None


def get_imports_from_file(path):
    with open(path, 'r') as file:
        root = _get_ast_from_file(file_content=file.read())

    if not root:
        return []

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
        root = _get_ast_from_file(file_content=file.read())

    if not root:
        return []

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


def is_imported_or_defined_in_file(*, stuff_to_import, vim_buffer):
    file_content = '\n'.join(vim_buffer)

    if stuff_to_import not in file_content:
        return False

    module = _get_ast_from_file(file_content=file_content)

    if not module:
        return True

    for node in ast.iter_child_nodes(module):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            if stuff_to_import in [el.name for el in node.names]:
                return True

        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            if node.name == stuff_to_import:
                return True

        if isinstance(node, ast.Assign):
            if stuff_to_import in [el.id for el in node.targets]:
                return True

    return False
