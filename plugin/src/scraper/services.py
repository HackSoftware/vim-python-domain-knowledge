import os

from src.ast.utils import (
    get_ast_nodes_from_file_content,
    is_ast_import,
    is_ast_import_from,
    is_ast_class_def,
    is_ast_function_def,
    is_ast_assign,
    ast_class_to_class_obj,
    ast_function_to_function_obj,
    ast_import_and_import_from_to_import_objects,
)

from src.settings import CURRENT_DIRECTORY


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


def get_ast_from_file_content(file_content, path):
    imports = []
    class_definitions = []
    function_definitions = []

    nodes = get_ast_nodes_from_file_content(file_content)

    for node in nodes:
        is_import = is_ast_import(node)
        is_import_from = is_ast_import_from(node)
        is_class = is_ast_class_def(node)
        is_function = is_ast_function_def(node)

        if is_import or is_import_from:
            import_objects = ast_import_and_import_from_to_import_objects(
                ast_import=node,
                file_path=path
            )

            imports.extend(import_objects)

        if is_class:
            class_obj = ast_class_to_class_obj(ast_class=node, file_path=path)
            class_definitions.append(class_obj)

        if is_function:
            function_obj = ast_function_to_function_obj(ast_function=node, file_path=path)
            function_definitions.append(function_obj)

    return imports, class_definitions, function_definitions


def get_ast_objects_from_file(path):
    with open(path, 'r') as file:
        return get_ast_from_file_content(file_content=file.read(), path=path)


def get_ast_objects_from_files(paths):
    imports = []
    class_definitions = []
    function_definitions = []

    for path in paths:
        imports_from_file, class_definitions_from_file, function_definitions_from_file = get_ast_objects_from_file(path)  # noqa

        imports.extend(imports_from_file)
        class_definitions.extend(class_definitions_from_file)
        function_definitions.extend(function_definitions_from_file)

    return imports, class_definitions, function_definitions


def is_imported_or_defined_in_file(*, stuff_to_import, vim_buffer):
    file_content = '\n'.join(vim_buffer)

    if stuff_to_import not in file_content:
        return False

    nodes = get_ast_nodes_from_file_content(file_content)

    for node in nodes:
        if is_ast_import(node) or is_ast_import_from(node):
            if stuff_to_import in [el.name for el in node.names]:
                return True

        if is_ast_function_def(node) or is_ast_class_def(node):
            if node.name == stuff_to_import:
                return True

        if is_ast_assign(node):
            if stuff_to_import in [el.id for el in node.targets]:
                return True

    return False
