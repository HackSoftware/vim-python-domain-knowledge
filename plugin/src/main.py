import os
from .settings import KNOWLEDGE_DIRECTORY
from .scraper import extract_all_imports, find_proper_line_for_import, is_import_in_file
from .database.services import setup_database, insert_imports, get_import_statement


def setup():
    if not os.path.isdir(KNOWLEDGE_DIRECTORY):
        os.mkdir(KNOWLEDGE_DIRECTORY)

    setup_database()

    imports = extract_all_imports()

    insert_imports(imports=imports)


def fill_import():
    import vim

    current_word = vim.eval('expand("<cword>")')

    current_buffer = vim.current.buffer
    current_window = vim.current.window
    cursor_current_row, cursor_current_col = current_window.cursor


    import_statement = get_import_statement(obj_to_import=current_word)

    if import_statement:
        if is_import_in_file(import_statement=import_statement['raw'], vim_buffer=current_buffer):
            print(f'"{current_word}" is already imported')
            return

        line_to_insert_import = find_proper_line_for_import(
            path=current_buffer.name,
            module_name=import_statement['module']
        )
        current_buffer.append(import_statement['raw'], line_to_insert_import)
        current_window.cursor = (cursor_current_row + 1, cursor_current_col)
