import ast


def ast_parse_file_content(file_content):
    try:
        return ast.parse(file_content)
    except Exception:
        return None


def get_ast_nodes_from_file_content(file_content):
    ast_root = ast_parse_file_content(file_content)
    if ast_root:
        try:
            return list(ast.iter_child_nodes(ast_root))
        except Exception:
            return []
