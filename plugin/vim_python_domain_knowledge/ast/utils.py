from typing import Optional, Union, List
from copy import deepcopy
import math

import ast

from vim_python_domain_knowledge.common.data_structures import Import, Class, Function
from vim_python_domain_knowledge.common.utils import (
    get_python_module_str_from_filepath,
    before_first_blank_line_after_line_or_end_line,
)
from vim_python_domain_knowledge.database.selectors import get_distinct_modules


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


def ast_class_to_class_obj(ast_class: ast.ClassDef, file_path: str) -> Class:
    parents = []
    for base in getattr(ast_class, 'bases', []):
        if is_ast_name(base):
            parents.append(base.id)

        if is_ast_attribute(base):
            parents.append(base.attr)

    return Class(
        file_path=file_path,
        name=ast_class.name,
        parents=parents,
        module=get_python_module_str_from_filepath(file_path)
    )


def ast_function_to_function_obj(ast_function: ast.FunctionDef, file_path: str) -> Function:
    return Function(
        file_path=file_path,
        name=ast_function.name,
        module=get_python_module_str_from_filepath(file_path),
        arguments=[
            *[el.arg for el in ast_function.args.args],
            *[el.arg for el in ast_function.args.kwonlyargs],
        ]
    )


def ast_import_and_import_from_to_import_objects(
    ast_import: Union[ast.Import, ast.ImportFrom],
    file_path
) -> List[Import]:
    is_import = is_ast_import(ast_import)
    is_import_from = is_ast_import_from(ast_import)

    if is_import:
        module = []

    is_relative = False

    if is_import_from:
        module = ''

        if ast_import.module:
            # level > 0 means that import is relative
            is_relative = ast_import.level and ast_import.level > 0
            module = ast_import.module.split('.')

    return [
        Import(
            module=module,
            name=el.name.split('.'),
            alias=el.asname,
            is_relative=is_relative
        )
        for el in ast_import.names
    ]


def should_be_added_to_import(
    file_content: str,
    import_name: str,
    file_path: str
) -> Optional[Union[ast.Import, ast.ImportFrom]]:
    """
    Returns the ast import in file that the "import_name" should be added to

    TODO: Think of a better name for this function?
    """
    nodes = get_ast_nodes_from_file_content(file_content=file_content)
    found_import_modules = get_distinct_modules(
        import_name=import_name
    )

    for node in nodes:
        if is_ast_import(node) or is_ast_import_from(node):
            import_objects = ast_import_and_import_from_to_import_objects(
                ast_import=node,
                file_path=file_path
            )

            matches = [
                '.'.join(import_obj.module) in found_import_modules  # Revisit that join
                for import_obj in import_objects
            ]

            if any(matches):
                return node


def get_modified_import(
    ast_import: Union[ast.Import, ast.ImportFrom],
    import_name: str
) -> Union[ast.Import, ast.ImportFrom]:
    modified_import = deepcopy(ast_import)
    modified_import.names.append(
        ast.alias(
            name=import_name,
            asname=None
        )
    )
    return modified_import


def are_imports_equal(
    imp1: Union[ast.Import, ast.ImportFrom],
    imp2: Union[ast.Import, ast.ImportFrom]
) -> bool:
    # imp1 and imp2 should be from the same file
    # Compare types just for sanity check
    if type(imp1) != type(imp2):
        return False

    return imp1.lineno == imp2.lineno


def get_modified_imports_and_lines_to_replace(
    file_content: str,
    ast_import: ast.Import,
    import_name: str
):
    start_line = ast_import.lineno
    end_line = None
    modified_import = get_modified_import(
        ast_import=ast_import,
        import_name=import_name
    )

    nodes = get_ast_nodes_from_file_content(file_content=file_content)

    nodes_count = len(nodes)

    for idx, node in enumerate(nodes):
        if is_ast_import(node) or is_ast_import_from(node):
            if are_imports_equal(node, ast_import):
                before_first_blank_line_after_the_node_or_end_line = before_first_blank_line_after_line_or_end_line(
                    file_content=file_content,
                    lineno=node.lineno
                )
                next_node_lineno = math.inf  # will be ignored if it's last node

                if idx < nodes_count:
                    next_node_lineno = nodes[idx + 1].lineno

                end_line = min(
                    next_node_lineno,
                    before_first_blank_line_after_the_node_or_end_line
                ) - 1

                return modified_import, start_line, end_line

    return None, None, None


def ast_import_to_lines_str(ast_import: ast.ImportFrom) -> List[str]:
    names = []

    for name in ast_import.names:
        if name.asname:
            names.append(f'{name.name} as {name.asname}')
        else:
            names.append(f'{name.name}')

    names_str = ', '.join(names)

    one_line_import = f'from {ast_import.module} import {names_str}'

    if len(one_line_import) <= 80:
        return [one_line_import, '']

    return [
        f'from {ast_import.module} import (',
        *[f'    {name},' for name in names],
        ')',
    ]


def get_new_import_proper_line_to_fit(file_content: str, module_name: str):
    def sort_import_function(ast_import):
        max_match = 0

        existing_import_name = getattr(ast_import, 'module', None)

        if not existing_import_name:
            return 0

        for i in range(len(existing_import_name) + 1):
            if module_name[:i] in existing_import_name or existing_import_name[:i] in module_name:
                if i > max_match:
                    max_match = i

        return max_match

    # Sanity check that file is valid
    root = ast_parse_file_content(file_content=file_content)
    if root is None:
        error_msg = 'Invalid syntax in file. Unable to fill import'
        raise Exception(error_msg)

    nodes = get_ast_nodes_from_file_content(file_content)

    imports = [
        node for node in nodes
        if is_ast_import(node) or is_ast_import_from(node)
    ]

    sorted_imports = sorted(imports, key=sort_import_function, reverse=True)

    if not list(sorted_imports):
        return 1

    most_simiar_import = sorted_imports[0]

    should_be_imported_after = module_name > most_simiar_import.module

    if not should_be_imported_after:
        return most_simiar_import.lineno

    nodes_count = len(nodes)

    for idx, node in enumerate(nodes):
        if is_ast_import(node) or is_ast_import_from(node):
            if are_imports_equal(node, most_simiar_import):
                before_first_blank_line_after_the_node_or_end_line = before_first_blank_line_after_line_or_end_line(
                    file_content=file_content,
                    lineno=node.lineno
                )
                next_node_lineno = math.inf  # will be ignored if it's last node

                if idx < nodes_count:
                    next_node_lineno = nodes[idx + 1].lineno

                return min(
                    next_node_lineno,
                    before_first_blank_line_after_the_node_or_end_line
                )

    return 1
