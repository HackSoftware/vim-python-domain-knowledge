from typing import List

from src.common.data_structures import Import, Class, Function

from .base import _get_db_connection
from .constants import DB_TABLES


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
        parents TEXT
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
        name TEXT
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


def setup_dictionary(classes: List[Class], functions: List[Function]):
    from ..settings import DICTIONARY_PATH

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

        classes_values.append(
            f'("{class_obj.file_path}", "{class_obj.name}", "{parents_str}")'
        )

    classes_str = ', '.join(classes_values)

    query = f'''
    INSERT INTO {DB_TABLES.CLASS_DEFINITIONS}
        (FILE_PATH, NAME, PARENTS)
        VALUES {classes_str}
    '''

    return _run_query(query)


def insert_functions(functions: List[Function]):
    functions_values = []

    for function_obj in functions:
        functions_values.append(
            f'("{function_obj.file_path}", "{function_obj.name}")'
        )

    functions_str = ', '.join(functions_values)

    query = f'''
    INSERT INTO {DB_TABLES.FUNCTION_DEFINITIONS}
        (FILE_PATH, NAME)
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
