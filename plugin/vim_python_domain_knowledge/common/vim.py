import vim


class Vim:
    @classmethod
    def eval(cls, *args, **kwargs):
        return vim.eval(*args, **kwargs)

    @classmethod
    def get_current_buffer(cls):
        return vim.current.buffer

    @classmethod
    def get_current_window(cls):
        return vim.current.window

    @classmethod
    def insert_at_line(cls, import_statement, line):
        current_buffer = cls.get_current_buffer()
        current_window = cls.get_current_window()
        cursor_current_row, cursor_current_col = current_window.cursor

        current_buffer.append(import_statement, line)
        current_window.cursor = (cursor_current_row + 1, cursor_current_col)
