import os
from vim_python_domain_knowledge.common.vim import Vim
from vim_python_domain_knowledge.common.utils import get_import_str_from_import_obj
from vim_python_domain_knowledge.settings import KNOWLEDGE_DIRECTORY
from vim_python_domain_knowledge.scraper import (
    extract_ast,
    get_ast_from_file_content,
    is_imported_or_defined_in_file,
)
from vim_python_domain_knowledge.database import (
    setup_database,
    insert_imports,
    insert_classes,
    insert_functions,
    get_absolute_import_statement,
    get_class,
    get_function,
    update_classes_for_file,
    update_functions_for_file,
    get_autocomletion_options,
    get_search_options,
    get_absolute_import_statement_by_alias,
    get_function_by_id,
    get_class_by_id,
)
from vim_python_domain_knowledge.ast.utils import (
    ast_import_to_lines_str,
    should_be_added_to_import,
    get_new_import_proper_line_to_fit,
    get_modified_imports_and_lines_to_replace,
)


def refresh_from_file():
    vim_buffer = Vim.get_current_buffer()
    file_content = '\n'.join(vim_buffer)
    imports, classes, functions = get_ast_from_file_content(
        file_content=file_content,
        path=vim_buffer.name
    )
    # TODO: Update imports probably?

    if classes:
        update_classes_for_file(classes=classes, file_path=vim_buffer.name)

    if functions:
        update_functions_for_file(
            functions=functions,
            file_path=vim_buffer.name
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


def fill_import():
    current_word = Vim.eval('expand("<cword>")')

    current_buffer = Vim.get_current_buffer()
    file_content = '\n'.join(current_buffer)

    already_imported = is_imported_or_defined_in_file(
        stuff_to_import=current_word,
        vim_buffer=current_buffer
    )

    if already_imported:
        print(f'"{current_word}" is already visible in file scope')
        return

    import_to_modify = should_be_added_to_import(
        file_content=file_content,
        import_name=current_word,
        file_path=current_buffer.name
    )

    # Put the new stuff in existing import
    if import_to_modify:
        ast_import, start_line, end_line = get_modified_imports_and_lines_to_replace(
            file_content=file_content,
            ast_import=import_to_modify,
            import_name=current_word
        )

        if ast_import:
            import_str_arr = ast_import_to_lines_str(ast_import=ast_import)
            current_buffer[start_line-1:end_line] = import_str_arr
            return

    # Import cannot be fit in existing import. A new one will be created
    # Step 1: Search in the existing imports
    import_obj = get_absolute_import_statement(
        obj_to_import=current_word
    )

    if import_obj:
        line_to_insert_import = get_new_import_proper_line_to_fit(
            file_content=file_content,
            module_name=import_obj.module
        )

        import_statement = get_import_str_from_import_obj(import_obj=import_obj)

        Vim.insert_at_line(
            import_statement=import_statement,
            line=(line_to_insert_import - 1)
        )
        return

    # Step 2: Search in class definitions
    class_obj = get_class(class_name=current_word)

    if class_obj:
        line_to_insert_import = get_new_import_proper_line_to_fit(
            file_content=file_content,
            module_name=class_obj.module
        )

        import_statement = f'from {class_obj.module} import {current_word}'

        Vim.insert_at_line(
            import_statement=import_statement,
            line=(line_to_insert_import - 1)
        )
        return

    # Step 3: Search in class definitions
    function_obj = get_function(function_name=current_word)

    if function_obj:
        line_to_insert_import = get_new_import_proper_line_to_fit(
            file_content=file_content,
            module_name=function_obj.module
        )

        import_statement = f'from {function_obj.module} import {current_word}'

        Vim.insert_at_line(
            import_statement=import_statement,
            line=(line_to_insert_import - 1)
        )
        return

    # Step 4: Search in imports with aliases (only if not found)
    import_obj_with_alias = get_absolute_import_statement_by_alias(
        obj_to_import=current_word
    )

    if import_obj_with_alias:
        line_to_insert_import = get_new_import_proper_line_to_fit(
            file_content=file_content,
            module_name=import_obj_with_alias.module
        )

        import_statement = get_import_str_from_import_obj(import_obj=import_obj_with_alias)

        Vim.insert_at_line(
            import_statement=import_statement,
            line=(line_to_insert_import - 1)
        )
        return




    print(f'Cannot find "{current_word}" export in the project :(')


def get_autocompletions_options_str():
    complete_options = get_autocomletion_options()
    options_str = [
        (
            '{'
            f'"icase": "{opt["icase"]}",'
            f'"word": "{opt["word"]}",'
            f'"abbr": "{opt["abbr"]}",'
            f'"menu": "{opt["menu"]}",'
            f'"info": "{opt["info"]}",'
            f'"empty": "{opt["empty"]}",'
            f'"dup": "{opt["dup"]}"'
            '}'
        )
        for opt in complete_options
    ]

    first_part = 'let l:data = ['
    content = ','.join(options_str)
    last_part = ']'

    return f'{first_part} {content} {last_part}'


def get_search_options_str():
    search_options = get_search_options()

    return '[' + ','.join([f"'{opt}'" for opt in search_options]) + ']'


def navigate_to_file_by_search_obj_id(obj_id):
    file_path = None

    if obj_id.startswith('c'):
        class_obj = get_class_by_id(class_id=obj_id[1:])

        if class_obj:
            Vim.go_to_file(class_obj.file_path, 1)

        return

    if obj_id.startswith('f'):
        function_obj = get_function_by_id(function_id=obj_id[:1])

        if function_obj:
            Vim.go_to_file(function_obj.file_path, 1)

        return
