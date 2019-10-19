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
