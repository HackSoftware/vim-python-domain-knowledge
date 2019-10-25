import os
from src.common.vim import Vim
from src.common.utils import get_import_str_from_import_obj
from src.settings import KNOWLEDGE_DIRECTORY
from src.scraper import (
    extract_ast,
    get_ast_from_file_content,
    find_proper_line_for_import,
    is_imported_or_defined_in_file,
)
from src.database import (
    setup_database,
    setup_dictionary,
    insert_imports,
    insert_classes,
    insert_functions,
    get_absolute_import_statement,
    get_class,
    get_function,
    update_classes_for_file,
    update_functions_for_file,
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

    setup_dictionary()


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

    setup_dictionary()


def fill_import():
    current_word = Vim.eval('expand("<cword>")')

    current_buffer = Vim.get_current_buffer()

    already_imported = is_imported_or_defined_in_file(
        stuff_to_import=current_word,
        vim_buffer=current_buffer
    )

    if already_imported:
        print(f'"{current_word}" is already visible in file scope')
        return

    # Step 1: Search in the existing imports
    import_obj = get_absolute_import_statement(
        obj_to_import=current_word
    )

    if import_obj:
        line_to_insert_import = find_proper_line_for_import(
            buffer=current_buffer,
            module_name=import_obj.module
        )
        import_statement = get_import_str_from_import_obj(import_obj=import_obj)

        Vim.insert_at_line(
            import_statement=import_statement,
            line=line_to_insert_import
        )
        return

    # Step 2: Search in class definitions
    class_obj = get_class(class_name=current_word)

    if class_obj:
        line_to_insert_import = find_proper_line_for_import(
            buffer=current_buffer,
            module_name=class_obj.module
        )

        import_statement = f'from {class_obj.module} import {current_word}'

        Vim.insert_at_line(
            import_statement=import_statement,
            line=line_to_insert_import
        )
        return

    # Step 3: Search in class definitions
    function_obj = get_function(function_name=current_word)

    if function_obj:
        line_to_insert_import = find_proper_line_for_import(
            buffer=current_buffer,
            module_name=function_obj.module
        )

        import_statement = f'from {function_obj.module} import {current_word}'

        Vim.insert_at_line(
            import_statement=import_statement,
            line=line_to_insert_import
        )
        return

    print(f'Cannot find "{current_word}" export in the project :(')
