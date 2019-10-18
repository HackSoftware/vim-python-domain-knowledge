import os
from .settings import KNOWLEDGE_DIRECTORY, CURRENT_DIRECTORY
from .scraper import (
    extract_all_imports,
    extract_all_exports,
    find_proper_line_for_import,
    is_imported_or_defined_in_file
)
from .database.services import (
    setup_database,
    setup_dictionary,
    insert_imports,
    get_import_statement,
    get_export_statement,
    insert_exports
)


def setup():
    if not os.path.isdir(KNOWLEDGE_DIRECTORY):
        os.mkdir(KNOWLEDGE_DIRECTORY)

    setup_database()

    imports = extract_all_imports()
    insert_imports(imports=imports)

    exports = list(extract_all_exports())
    insert_exports(exports=exports)

    setup_dictionary(exports=exports)


def fill_import():
    import vim

    current_word = vim.eval('expand("<cword>")')

    current_buffer = vim.current.buffer
    current_window = vim.current.window
    cursor_current_row, cursor_current_col = current_window.cursor

    already_imported = is_imported_or_defined_in_file(
        stuff_to_import=current_word,
        vim_buffer=current_buffer
    )
    if already_imported:
        print(f'"{current_word}" is already visible in file scope')
        return

    # Step 1: Search in the existing imports
    import_statement = get_import_statement(obj_to_import=current_word)

    if import_statement:
        line_to_insert_import = find_proper_line_for_import(
            buffer=current_buffer,
            module_name=import_statement['module']
        )

        current_buffer.append(import_statement['raw'], line_to_insert_import)
        current_window.cursor = (cursor_current_row + 1, cursor_current_col)

        return

    # Step 2: Search in the existing exportss
    export_statement = get_export_statement(export_name=current_word)
    if export_statement:
        source = export_statement['path']\
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
