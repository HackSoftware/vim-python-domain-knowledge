from vim_python_domain_knowledge.settings import CURRENT_DIRECTORY

from vim_python_domain_knowledge.common.data_structures import Import


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


def before_first_blank_line_after_line_or_end_line(file_content: str, lineno: int) -> str:
    lines = file_content.split('\n')
    blank_lines_numbers_after_lineno = [
        idx + 1 for idx,
        line in enumerate(lines)
        if idx > int(lineno) and line == ''
    ]

    if blank_lines_numbers_after_lineno:
        return blank_lines_numbers_after_lineno[0]

    return len(lines)
