from src.settings import CURRENT_DIRECTORY


def get_python_module_str_from_filepath(file_path):
    return file_path\
        .replace(f'{CURRENT_DIRECTORY}/', '')\
        .replace('.py', '')\
        .replace('/', '.')
