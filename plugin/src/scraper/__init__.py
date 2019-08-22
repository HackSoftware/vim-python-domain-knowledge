from .services import (
    find_all_files,
    get_imports_from_files
)


def extract_all_imports():
    python_files = find_all_files()
    print(python_files)

    return get_imports_from_files(python_files)


__all__ = [
    'extract_all_imports',
]
