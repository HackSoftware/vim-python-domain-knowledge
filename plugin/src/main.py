import os
from .settings import KNOWLEDGE_DIRECTORY
from .scraper import extract_all_imports
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
        # Import at the beginning at the file
        # TODO: This is a temporary implementation... Find the exact place to put the import
        current_buffer.append(import_statement, 0)
        current_window.cursor = (cursor_current_row + 1, cursor_current_col)
