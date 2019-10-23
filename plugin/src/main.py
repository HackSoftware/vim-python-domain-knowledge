import os
from src.common.vim import Vim
from src.settings import KNOWLEDGE_DIRECTORY, CURRENT_DIRECTORY
from src.scraper import (
    extract_ast,
    extract_all_exports,
    find_proper_line_for_import,
    is_imported_or_defined_in_file
)
from src.database import (
    setup_database,
    setup_dictionary,
    insert_imports,
    insert_classes,
    insert_functions,
    get_absolute_import_statement,
    get_export_statement,
    insert_exports,
    get_class,
    get_function
)


def setup():
    if not os.path.isdir(KNOWLEDGE_DIRECTORY):
        os.mkdir(KNOWLEDGE_DIRECTORY)

    setup_database()

    imports, classes, functions = extract_ast()

    if imports:
        insert_imports(imports=imports)

    if classes:
        insert_classes(classes=classes)

    if functions:
        insert_functions(functions=functions)

    exports = list(extract_all_exports())
    insert_exports(exports=exports)

    setup_dictionary(exports=exports)


def fill_import():
    current_word = Vim.eval('expand("<cword>")')

    current_buffer = Vim.get_current_buffer()
    current_window = Vim.get_current_window()
    cursor_current_row, cursor_current_col = current_window.cursor

    already_imported = is_imported_or_defined_in_file(
        stuff_to_import=current_word,
        vim_buffer=current_buffer
    )
    if already_imported:
        print(f'"{current_word}" is already visible in file scope')
        return

    # Step 1: Search in the existing imports
    import_statement = get_absolute_import_statement(obj_to_import=current_word)

    if import_statement:
        line_to_insert_import = find_proper_line_for_import(
            buffer=current_buffer,
            module_name=import_statement['module']
        )

        current_buffer.append(import_statement['raw'], line_to_insert_import)
        current_window.cursor = (cursor_current_row + 1, cursor_current_col)

        return

    # Step 2: Search in class definitions
    class_obj = get_class(class_name=current_word)

    if class_obj:
        source = class_obj.file_path\
            .replace(CURRENT_DIRECTORY, '')\
            .replace('.py', '')\
            .replace('/', '.')

        if source.startswith('.'):
            source = source[1:]

        line_to_insert_import = find_proper_line_for_import(
            buffer=current_buffer,
            module_name=source
        )

        import_statement = f'from {source} import {current_word}'

        current_buffer.append(import_statement, line_to_insert_import)
        current_window.cursor = (cursor_current_row + 1, cursor_current_col)
        return

    # Step 3: Search in class definitions
    function_obj = get_function(function_name=current_word)

    if function_obj:
        source = function_obj.file_path\
            .replace(CURRENT_DIRECTORY, '')\
            .replace('.py', '')\
            .replace('/', '.')

        if source.startswith('.'):
            source = source[1:]

        line_to_insert_import = find_proper_line_for_import(
            buffer=current_buffer,
            module_name=source
        )

        import_statement = f'from {source} import {current_word}'

        current_buffer.append(import_statement, line_to_insert_import)
        current_window.cursor = (cursor_current_row + 1, cursor_current_col)
        return

    print(f'Cannot find "{current_word}" export in the project :(')
