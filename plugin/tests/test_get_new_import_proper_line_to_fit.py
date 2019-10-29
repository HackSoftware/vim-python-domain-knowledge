from unittest import TestCase

from vim_python_domain_knowledge.ast.utils import get_new_import_proper_line_to_fit


class FillImportInFileWithNoImportsTests(TestCase):
    def test_fill_import_in_empty_file(self):
        module = 'test.module'
        file_content = ''
        self.assertEqual(
            1,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )

    def test_fill_import_in_file_with_no_imports(self):
        module = 'test.module'
        lines = [
            'def some_func():',
            '    pass',
        ]
        file_content = '\n'.join(lines)

        self.assertEqual(
            1,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )


class FillImportBetweenTwoImportsTests(TestCase):
    def test_single_line_imports(self):
        module = 'bmodule'

        lines = [
            'from amodule import something',
            'from another_source import something',
            '',
            'def some_func():',
            '    pass',
        ]

        file_content = '\n'.join(lines)

        self.assertEqual(
            2,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )

    def test_multi_line_imports(self):
        module = 'bmodule'

        lines = [
            'from amodule import (',
            '    something',
            ')',
            'from another_source import (',
            '    something',
            ')',
            '',
            '',
            'def some_func():',
            '    pass',
        ]
        file_content = '\n'.join(lines)

        self.assertEqual(
            4,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )


class FillImportBetweenTwoImportsWithEmptyLinesBetweenTests(TestCase):
    def test_single_line_imports(self):
        module = 'bmodule'

        lines = [
            'from amodule import something',
            '',
            'from cmodule import something',
            '',
            'def some_func():',
            '    pass',
        ]
        file_content = '\n'.join(lines)

        self.assertEqual(
            3,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )

    def test_multi_line_imports(self):
        module = 'bmodule'

        lines = [
            'from amodule import (',
            '    something',
            ')',
            '',
            'from cmodule import (',
            "    something",
            ")",
            '',
            '',
            'def some_func():',
            '    pass',
        ]

        file_content = '\n'.join(lines)

        self.assertEqual(
            4,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )


class FillImportInTheBeginningInFileWithImports(TestCase):
    def test_single_line_import(self):
        module = 'amodule'

        lines = [
            'from bmodule import something',
            '',
            'def some_func():',
            '    pass',
        ]

        file_content = '\n'.join(lines)

        self.assertEqual(
            1,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )

    def test_multi_line_import(self):
        module = 'amodule'

        lines = [
            'from bmodule import (',
            '    something',
            ')',
            '',
            'def some_func():',
            '    pass',
        ]

        file_content = '\n'.join(lines)

        self.assertEqual(
            1,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )

    def test_single_line_import_with_empty_line_before(self):
        module = 'amodule'

        lines = [
            '',
            'from bmodule import something',
            '',
            'def some_func():',
            '    pass',
        ]

        file_content = '\n'.join(lines)

        self.assertEqual(
            2,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )

    def test_multi_line_import_with_empty_line_before(self):
        module = 'amodule'

        lines = [
            '',
            'from bmodule import (',
            '    something',
            ')',
            '',
            'def some_func():',
            '    pass',
        ]

        file_content = '\n'.join(lines)

        self.assertEqual(
            2,
            get_new_import_proper_line_to_fit(
                file_content=file_content,
                module_name=module
            )
        )
