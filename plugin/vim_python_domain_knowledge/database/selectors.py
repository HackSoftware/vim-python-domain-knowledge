from typing import Optional, List

from .base import _get_db_connection
from .constants import DB_TABLES
from vim_python_domain_knowledge.common.data_structures import Class, Function, Import


def get_absolute_import_statement(obj_to_import: str) -> Import:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT id, module, name, alias, is_relative, lineno
            FROM {DB_TABLES.IMPORTS}
            WHERE name=? and is_relative=0
            GROUP BY module
            ORDER BY COUNT(*) DESC
        ''',
        (obj_to_import, )
    )

    result = cursor.fetchone()

    if result:
        return Import(*result)


def get_absolute_import_statement_by_alias(obj_to_import: str) -> Import:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT id, module, name, alias, is_relative, lineno
            FROM {DB_TABLES.IMPORTS}
            WHERE alias=? and is_relative=0
            GROUP BY module
            ORDER BY COUNT(*) DESC
        ''',
        (obj_to_import, )
    )

    result = cursor.fetchone()

    if result:
        return Import(*result)


def get_all_classes():
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT id, file_path, name, parents, module, lineno
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
        SELECT id, file_path, name, module, arguments, lineno
            FROM {DB_TABLES.FUNCTION_DEFINITIONS}
        ''',
    )

    result = cursor.fetchall()

    return [
        Function(*el)
        for el in result
    ]


def get_class_by_id(class_id: int) -> Optional[Class]:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT id, file_path, name, parents, module, lineno
            FROM {DB_TABLES.CLASS_DEFINITIONS}
            WHERE id=?
        ''',
        (class_id, )
    )

    result = cursor.fetchone()

    if result:
        return Class(*result)


def get_class(class_name: str) -> Optional[Class]:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT id, file_path, name, parents, module, lineno
            FROM {DB_TABLES.CLASS_DEFINITIONS}
            WHERE name=?
        ''',
        (class_name, )
    )

    result = cursor.fetchone()

    if result:
        return Class(*result)


def get_function_by_id(function_id: int) -> Optional[Function]:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT id, file_path, name, module, arguments, lineno
            FROM {DB_TABLES.FUNCTION_DEFINITIONS}
            WHERE id=?
        ''',
        (function_id, )
    )

    result = cursor.fetchone()

    if result:
        return Function(*result)


def get_function(function_name: str) -> Optional[Function]:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT id, file_path, name, module, arguments, lineno
            FROM {DB_TABLES.FUNCTION_DEFINITIONS}
            WHERE name=?
        ''',
        (function_name, )
    )

    result = cursor.fetchone()

    if result:
        return Function(*result)


def get_distinct_absolute_import_statements_modules(
    import_name: str
) -> List[str]:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT DISTINCT module
            FROM {DB_TABLES.IMPORTS}
            WHERE name = "{import_name}"
        ''',
    )

    result = cursor.fetchall()

    return [el[0] for el in result]


def get_distinct_classes_modules(
    import_name: str
) -> List[str]:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT DISTINCT module
            FROM {DB_TABLES.CLASS_DEFINITIONS}
            WHERE name = "{import_name}"
        ''',
    )

    result = cursor.fetchall()

    return [el[0] for el in result]


def get_distinct_functions_modules(
    import_name: str
) -> List[str]:
    connection = _get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        f'''
        SELECT DISTINCT module
            FROM {DB_TABLES.FUNCTION_DEFINITIONS}
            WHERE name = "{import_name}"
        ''',
    )

    result = cursor.fetchall()

    return [el[0] for el in result]


def get_distinct_modules(import_name: str) -> List[str]:
    """
    Returns list of uniques modules searching in:
        - all imports
        - all class definitions
        - all functions
    """
    modules = [
        *get_distinct_absolute_import_statements_modules(import_name=import_name),
        *get_distinct_classes_modules(import_name=import_name),
        *get_distinct_functions_modules(import_name=import_name),
    ]

    return list(set(modules))
