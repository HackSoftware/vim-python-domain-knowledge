from .services import (
    find_all_files,
    get_imports_from_files,
    find_proper_line_for_import,
    is_import_in_file
)


def extract_all_imports():
    python_files = find_all_files()

    return get_imports_from_files(python_files)


__all__ = [
    'extract_all_imports',
]
