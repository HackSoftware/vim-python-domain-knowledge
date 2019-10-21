from .base import _get_db_connection


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


def get_export_statement(export_name: str):
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT path, name
            FROM exports
            WHERE name=?
        ''',
        (export_name, )
    )

    result = cursor.fetchone()

    if result:
        return {
            'path': result[0],
            'name': result[1]
        }
