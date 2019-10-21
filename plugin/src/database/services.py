from typing import List

from src.common.data_structures import Import, Export

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
        alias TEXT
    )
    '''
    return _run_query(create_table_query)


def _create_exports_table():
    drop_table_query = f'''
    DROP TABLE IF EXISTS {DB_TABLES.EXPORTS}
    '''
    _run_query(drop_table_query)

    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {DB_TABLES.EXPORTS} (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        path TEXT,
        name TEXT,
        type TEXT
    )
    '''
    return _run_query(create_table_query)


def setup_database():
    # Create database
    _get_db_connection()

    # Create tables
    _create_imports_table()
    _create_exports_table()


def setup_dictionary(exports: List[Export]):
    from ..settings import DICTIONARY_PATH

    with open(DICTIONARY_PATH, 'w') as file:
        for export in exports:
            file.write(f'{export.name}\n')


def insert_imports(imports: List[Import]):
    imports_values = [
        f'("{".".join(obj.module)}", "{".".join(obj.name)}", "{obj.alias or ""}")'  # noqa
        for obj in imports
    ]
    imports_str = ', '.join(imports_values)

    query = f'''
    INSERT INTO {DB_TABLES.IMPORTS}
        (MODULE, NAME, ALIAS)
        VALUES {imports_str}
    '''

    return _run_query(query)


def insert_exports(exports: List[Export]):
    exports_values = [
        f'("{obj.path}", "{obj.name}", "{obj.type}")'
        for obj in exports
    ]
    exports_str = ', '.join(exports_values)

    query = f'''
    INSERT INTO {DB_TABLES.EXPORTS}
        (PATH, NAME, TYPE)
        VALUES {exports_str}
    '''

    return _run_query(query)
