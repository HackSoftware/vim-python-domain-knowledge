from .services import (
    find_all_files,
    get_ast_objects_from_files,
    is_imported_or_defined_in_file,
    get_ast_from_file_content
)


def extract_ast():
    python_files = find_all_files()

    return get_ast_objects_from_files(python_files)


__all__ = [
    'extract_ast',
    'is_imported_or_defined_in_file',
    'get_ast_from_file_content'
]
