from typing import List

from src.common.data_structures import Import, Class, Function

from .base import _get_db_connection
from .constants import DB_TABLES
from .selectors import get_all_classes, get_all_functions


def _run_query(query: str):
    connection = _get_db_connection()
    connection.execute(query)
    connection.commit()


def _create_imports_table():
    drop_table_query = f'''
    DROP TABLE IF EXISTS {DB_TABLES.IMPORTS}
    '''
    _run_query(drop_table_query)

    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {DB_TABLES.IMPORTS} (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        module TEXT,
        name TEXT,
        alias TEXT,
        is_relative BOOLEAN
    )
    '''
    return _run_query(create_table_query)


def _create_class_definitions_table():
    drop_table_query = f'''
    DROP TABLE IF EXISTS {DB_TABLES.CLASS_DEFINITIONS}
    '''
    _run_query(drop_table_query)

    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {DB_TABLES.CLASS_DEFINITIONS} (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        file_path TEXT,
        name TEXT,
        parents TEXT,
        module TEXT
    )
    '''
    return _run_query(create_table_query)


def _create_function_definitions_table():
    drop_table_query = f'''
    DROP TABLE IF EXISTS {DB_TABLES.FUNCTION_DEFINITIONS}
    '''
    _run_query(drop_table_query)

    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {DB_TABLES.FUNCTION_DEFINITIONS} (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        file_path TEXT,
        name TEXT,
        module TEXT
    )
    '''
    return _run_query(create_table_query)


def setup_database():
    # Create database
    _get_db_connection()

    # Create tables
    _create_imports_table()
    _create_class_definitions_table()
    _create_function_definitions_table()


def get_autocomletion_options():
    classes = get_all_classes()
    functions = get_all_functions()

    exports = []
    for class_obj in classes:
        exports.append([class_obj.name, class_obj.module])

    for function_obj in functions:
        exports.append([function_obj.name, function_obj.module])

    return sorted(exports)


def setup_dictionary():
    from ..settings import DICTIONARY_PATH
    classes = get_all_classes()
    functions = get_all_functions()

    exports = []
    for class_obj in classes:
        exports.append(f'{class_obj.name}\n')

    for function_obj in functions:
        exports.append(f'{function_obj.name}\n')

    with open(DICTIONARY_PATH, 'w') as file:
        for export in sorted(exports):
            file.write(f'{export}\n')


def insert_imports(imports: List[Import]):
    imports_values = []

    for import_obj in imports:
        module_str = '.'.join(import_obj.module)
        name_str = '.'.join(import_obj.name)
        alias_str = import_obj.alias or ''
        is_relative_str = '1' if import_obj.is_relative else '0'

        imports_values.append(
            f'("{module_str}", "{name_str}", "{alias_str}", "{is_relative_str}")'  # noqa
        )

    imports_str = ', '.join(imports_values)

    query = f'''
    INSERT INTO {DB_TABLES.IMPORTS}
        (MODULE, NAME, ALIAS, IS_RELATIVE)
        VALUES {imports_str}
    '''

    return _run_query(query)


def insert_classes(classes: List[Class]):
    classes_values = []

    for class_obj in classes:
        parents_str = ','.join(class_obj.parents)
        file_path = class_obj.file_path
        name = class_obj.name
        module = class_obj.module

        classes_values.append(
            f'("{file_path}", "{name}", "{parents_str}", "{module}")'
        )

    classes_str = ', '.join(classes_values)

    query = f'''
    INSERT INTO {DB_TABLES.CLASS_DEFINITIONS}
        (FILE_PATH, NAME, PARENTS, MODULE)
        VALUES {classes_str}
    '''

    return _run_query(query)


def insert_functions(functions: List[Function]):
    functions_values = []

    for function_obj in functions:
        file_path = function_obj.file_path
        name = function_obj.name
        module = function_obj.module

        functions_values.append(
            f'("{file_path}", "{name}", "{module}")'
        )

    functions_str = ', '.join(functions_values)

    query = f'''
    INSERT INTO {DB_TABLES.FUNCTION_DEFINITIONS}
        (FILE_PATH, NAME, MODULE)
        VALUES {functions_str}
    '''

    return _run_query(query)


def delete_classes_for_file(file_path):
    query = f'''
    DELETE FROM {DB_TABLES.CLASS_DEFINITIONS}
        WHERE FILE_PATH = "{file_path}"
    '''

    return _run_query(query)


def delete_functions_for_file(file_path):
    query = f'''
    DELETE FROM {DB_TABLES.FUNCTION_DEFINITIONS}
        WHERE FILE_PATH = "{file_path}"
    '''

    return _run_query(query)


def update_classes_for_file(classes: List[Class], file_path):
    delete_classes_for_file(file_path=file_path)
    insert_classes(classes=classes)


def update_functions_for_file(functions: List[Function], file_path):
    delete_functions_for_file(file_path=file_path)
    insert_functions(functions=functions)
