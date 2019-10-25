from typing import Optional, Union, List

import ast

from src.common.data_structures import Import, Class, Function
from src.common.utils import get_python_module_str_from_filepath
from src.database.selectors import get_distinct_modules


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
        module=get_python_module_str_from_filepath(file_path)
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
