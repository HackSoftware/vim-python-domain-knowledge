import sqlite3
from typing import List
from ..scraper.services import Import, Export


def _get_db_connection():
    from ..settings import DB_PATH
    return sqlite3.connect(DB_PATH)


def _run_query(query: str):
    connection = _get_db_connection()
    connection.execute(query)
    connection.commit()


def _create_imports_table():
    drop_table_query = '''
    DROP TABLE IF EXISTS imports
    '''
    _run_query(drop_table_query)

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS imports (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        module TEXT,
        name TEXT,
        alias TEXT
    )
    '''
    return _run_query(create_table_query)


def _create_exports_table():
    drop_table_query = '''
    DROP TABLE IF EXISTS exports
    '''
    _run_query(drop_table_query)

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS exports (
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


def insert_imports(imports: List[Import]):
    imports_values = [
        f'("{".".join(obj.module)}", "{".".join(obj.name)}", "{obj.alias or ""}")'
        for obj in imports
    ]
    imports_str = ', '.join(imports_values)

    query = f'''
    INSERT INTO imports
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
    INSERT INTO exports
        (PATH, NAME, TYPE)
        VALUES {exports_str}
    '''

    return _run_query(query)


def get_import_statement(obj_to_import: str):
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT module, name
            FROM imports
            WHERE name=?
            GROUP BY module
            ORDER BY COUNT(*)
        ''',
        (obj_to_import, )
    )

    result = cursor.fetchone()

    if result:
        if result[0]:
            return {
                'raw': f'from {result[0]} import {result[1]}',
                'module': result[0]
            }

        return {
            'raw': f'import {result[1]}',
            'module': result[1]
        }
