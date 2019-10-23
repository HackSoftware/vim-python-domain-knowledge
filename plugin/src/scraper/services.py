import os
import ast

from src.common.data_structures import Import, Class, Function

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
    root = ast.parse(file_content)

    imports = []
    class_definitions = []
    function_definitions = []

    for node in ast.iter_child_nodes(root):
        is_import = isinstance(node, ast.Import)
        is_import_from = isinstance(node, ast.ImportFrom)
        is_class = isinstance(node, ast.ClassDef)
        is_function = isinstance(node, ast.FunctionDef)

        if is_import or is_import_from:
            if is_import:
                module = []

            is_relative = False

            if is_import_from:
                module = ''

                if node.module:
                    # level > 0 means that import is relative
                    is_relative = node.level and node.level > 0
                    module = node.module.split('.')

            for n in node.names:
                imports.append(
                    Import(
                        module=module,
                        name=n.name.split('.'),
                        alias=n.asname,
                        is_relative=is_relative
                    )
                )

        if is_class:
            parents = []
            for base in getattr(node, 'bases', []):
                if isinstance(base, ast.Name):
                    parents.append(base.id)

                if isinstance(base, ast.Attribute):
                    parents.append(base.attr)

            class_definitions.append(
                Class(
                    file_path=path,
                    name=node.name,
                    parents=parents
                )
            )

        if is_function:
            function_definitions.append(
                Function(
                    file_path=path,
                    name=node.name
                )
            )

    return imports, class_definitions, function_definitions


def get_ast_objects_from_file(path):
    with open(path, 'r') as file:
        return get_ast_from_file_content(file_content=file.read(), path=path)


def find_proper_line_for_import(buffer, module_name):
    # TODO: Rework this ? :(
    for line_number, line in enumerate(buffer):
        if module_name in line:
            return line_number

    return 0


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

    module = ast.parse(file_content)

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
