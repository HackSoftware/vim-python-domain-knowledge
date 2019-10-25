from typing import Optional

from .base import _get_db_connection
from .constants import DB_TABLES
from src.common.data_structures import Class, Function


def get_absolute_import_statement(obj_to_import: str):
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT module, name
            FROM {DB_TABLES.IMPORTS}
            WHERE name=? and is_relative=0
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


def get_all_classes():
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT file_path, name, parents, module
            FROM {DB_TABLES.CLASS_DEFINITIONS}
        ''',
    )

    result = cursor.fetchall()

    return [
        Class(*el)
        for el in result
    ]


def get_all_functions():
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT file_path, name, module
            FROM {DB_TABLES.FUNCTION_DEFINITIONS}
        ''',
    )

    result = cursor.fetchall()

    return [
        Function(*el)
        for el in result
    ]


def get_class(class_name: str) -> Optional[Class]:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT file_path, name, parents, module
            FROM {DB_TABLES.CLASS_DEFINITIONS}
            WHERE name=?
        ''',
        (class_name, )
    )

    result = cursor.fetchone()

    if result:
        return Class(*result)


def get_function(function_name: str) -> Optional[Function]:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT file_path, name, module
            FROM {DB_TABLES.FUNCTION_DEFINITIONS}
            WHERE name=?
        ''',
        (function_name, )
    )

    result = cursor.fetchone()

    if result:
        return Function(*result)
