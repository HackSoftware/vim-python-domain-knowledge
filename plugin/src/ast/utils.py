from typing import Optional, Union

import ast

from src.common.data_structures import Import


def is_ast_import(el) -> bool:
    return isinstance(el, ast.Import)


def is_ast_import_from(el) -> bool:
    return isinstance(el, ast.ImportFrom)


def is_ast_class_def(el) -> bool:
    return isinstance(el, ast.ClassDef)


def is_ast_function_def(el) -> bool:
    return isinstance(el, ast.FunctionDef)


def is_ast_name(el) -> bool:
    return isinstance(el, ast.Name)


def is_ast_attribute(el) -> bool:
    return isinstance(el, ast.Attribute)


def is_ast_assign(el) -> bool:
    return isinstance(el, ast.Assign)


def ast_parse_file_content(file_content):
    try:
        return ast.parse(file_content)
    except Exception:
        return None


def get_ast_nodes_from_file_content(file_content):
    ast_root = ast_parse_file_content(file_content)
    if ast_root:
        try:
            return list(ast.iter_child_nodes(ast_root))
        except Exception:
            return []
    return []


def should_be_added_to_import(file_content: str, import_obj: Import) -> Optional[Union[ast.Import, ast.ImportFrom]]:
    nodes = get_ast_nodes_from_file_content(file_content=file_content)
    for node in nodes:
        pass
