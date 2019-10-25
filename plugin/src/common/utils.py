from src.settings import CURRENT_DIRECTORY

from src.common.data_structures import Import


def get_python_module_str_from_filepath(file_path):
    return file_path\
        .replace(f'{CURRENT_DIRECTORY}/', '')\
        .replace('.py', '')\
        .replace('/', '.')


def get_import_str_from_import_obj(import_obj: Import) -> str:
    name = import_obj.name
    module = import_obj.module
    alias = import_obj.alias

    if module:
        if alias:
            return f'from {module} import {name} as {alias}'

        return f'from {module} import {name}'

    if alias:
        return f'import {name} as {alias}'

    return f'import {name}'
