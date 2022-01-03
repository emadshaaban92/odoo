# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" List all python/xml source lines which looks like a x2many command """

import ast
import functools
import pathlib
import sys
import subprocess
import re

sys.modules['_elementtree'] = None  # Force python XML
import xml.etree.ElementTree as ET

from odoo.modules.module import get_modules, get_module_path
from odoo.tests import BaseCase
from odoo.tools import file_open


SKIP_MODULES = {
    # 'base',
}

SKIP_FILES = {
    # 'test_new_api/models/test_new_api.py',
}


COMMANDS = ["create", "update", "delete", "unlink", "link", "clear", "set"]
x2many_func_map = ["Command." + cmd for cmd in COMMANDS]
x2many_const_map = ["Command." + cmd.upper() for cmd in COMMANDS]

OLD_COMMAND_STYLE_FOUND_MESSAGE = """\
Found old-style XMany command at %(path)s:%(lineno)s %(line)s
"""

REPLACEMENT_SUGGESTION_MESSAGE = """\
Suggested replacement:\n
%(replacement)s
"""


class _LineNumberingParser(ET.XMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.version)

    def _start(self, *args, **kwargs):
        # Here we assume the default XML parser which is expat
        # and copy its element position attributes into output Elements
        print('in')
        element = super()._start(*args, **kwargs)
        element._start_line_number = self.parser.CurrentLineNumber
        element._start_column_number = self.parser.CurrentColumnNumber
        element._start_byte_index = self.parser.CurrentByteIndex
        return element

    def _end(self, *args, **kwargs):
        element = super()._end(*args, **kwargs)
        element._end_line_number = self.parser.CurrentLineNumber
        element._end_column_number = self.parser.CurrentColumnNumber
        element._end_byte_index = self.parser.CurrentByteIndex
        return element


def _iszero(node):
    """ is ``node`` the literal int 0 """
    return type(node) is ast.Constant and node.value == 0


def _match_all(root):
    """
    Returns an iterable that yield every node likely to be an old-style
    x2many command. x2many commands are tuples enclosed in a list or a
    list comprehension that match any of those pep-0622-style cases:

        case (0, 0, _)
        case (1, _, _)
        case (2, _)
        case (2, _, 0)
        case (3, _)
        case (3, _, 0)
        case (4, _)
        case (4, _, 0)
        case (5,)
        case (5, 0)
        case (5, 0, 0)
        case (6, 0, _)
    """

    @functools.lru_cache()
    def match(node):
        if type(node) is not ast.Tuple:
            return False

        if not (1 <= len(node.elts) <= 3):
            return False

        if type(node.elts[0]) is not ast.Constant:
           return False

        val = node.elts[0].value
        if type(val) is not int:
           return False
        if not (0 <= val <= 6):
           return False

        if val in (0, 6):
            if len(node.elts) != 3:
                return False
            if not _iszero(node.elts[1]):
                return False

        elif val == 1:
            if len(node.elts) != 3:
                return False

        elif 2 <= val <= 4:
            if len(node.elts) == 1:
                return False
            elif len(node.elts) == 2:
                pass
            elif not _iszero(node.elts[2]):
                return False

        elif val == 5:
            if len(node.elts) == 1:
                pass
            elif len(node.elts) == 2 and _iszero(node.elts[1]):
                pass
            elif len(node.elts) == 3 and _iszero(node.elts[1]) and _iszero(node.elts[2]):
                pass
            else:
                return False

        return True

    for node in ast.walk(root):
        if type(node) is ast.List:
            if all(map(match, node.elts)):
                yield from node.elts

        if type(node) is ast.ListComp:
            if match(node.elt):
                yield node.elt


def rewrite(line):
    """ Return ``line`` with old-style commands replaced by new-style ones """
    # /!\ Highly experimental /!\

    watchdog = 5
    while True:
        match = re.search(r'\(([0-6]),', line)
        if not match:
            break

        code = int(match.group(1))
        cmd = x2many_func_map[code]

        if code in (0, 6):
            line = re.sub(r'\([06], ?(0|False|None), ?', f"{cmd}(", line, 1)
        elif code == 1:
            line = re.sub(r'\(1, ?', f"{cmd}(", line, 1)
        elif code in (2, 3, 4):
            line = re.sub(r'\([234], ?(.*?), ?(0|False|None)\)', f"{cmd}(\\1)", line, 1)
            line = re.sub(r'\([234], ?(.*?)\)', f"{cmd}(\\1)", line, 1)
        elif code == 5:
            line = re.sub(r'\(5,( ?(0|False|None)(, ?(0|False|None))?)?\)', f"{cmd}()", line, 1)
        else:
            raise SyntaxError("Cannot rewrite")

        watchdog -= 1
        if not watchdog:
            raise SyntaxError("Cannot rewrite")

    return line


def _python_read_parse(path):
    with file_open(path) as file:
        code = file.read()
        tree = ast.parse(code, filename=path)
        lines = code.splitlines()
    return lines, tree


def _python_fix_import(path, lines):
    """ Attempt to fix the file to include ``from odoo import Command`` """
    for lineno, line in zip(range(30), lines):
        if line.startswith('from odoo import'):
            return 'replace', lineno + 1, lines[lineno].rstrip() + ', Command'

    last_odoo_import = 0
    for lineno, line in zip(range(30), lines):
        if line.startswith('import odoo') or line.startswith('from odoo'):
            last_odoo_import = lineno

        elif last_odoo_import:
            return 'add', lineno + 1, "from odoo import Command"

    last_import = 0
    for lineno, line in zip(range(30), lines):
        if line.startswith('import ') or line.startswith('from '):
            last_odoo_import = lineno

        elif last_odoo_import:
            return 'add', lineno + 1, "from odoo import Command"

    raise SyntaxError("Cannot fix import")


def _xml_read_parse(path):
    with file_open(path, 'rb') as file:
        doc = file.read()
        tree = ET.fromstring(doc, parser=_LineNumberingParser())
        lines = doc.decode().splitlines()
    return lines, tree


def _xml_search_for_python(tree):    
    for field in tree.findall(r".//field[@eval]"):
        start_lineno = field._start_line_number - 1
        root = ast.parse(field.get('eval'))
        yield root, start_lineno


def x2many_lint(path, file_ext):
    if file_ext == 'py':
        read_parse = _python_read_parse
        search_for_python = lambda tree: [(tree, 0)]
    elif file_ext == 'xml':
        read_parse = _xml_read_parse
        search_for_python = _xml_search_for_python

    try:
        lines, tree = read_parse(path)
    except (SyntaxError, UnicodeDecodeError) as exc:
        logger.warning("Cannot parse %s. Maybe skip it?", path, exc_info=True)
        return

    changes = []
    for root, start_lineno in search_for_python(tree):
        for lineno in [start_lineno + node.lineno for node in _match_all(root)]:
            logger.warning("Found old-style x2Many command at %s:%s", path, lineno)
            with suppress(SyntaxError):
                changes.append(rewrite(lines[lineno - 1]))

    if not changes or file_ext != 'py':
        return

    with suppress(SyntaxError):
        changes.append(_python_fix_import(path, lines))

    suggested_lines = lines.copy()
    for lineno, line in ((c[1], c[2]) for c in changes if c[0] == 'replace'):
        suggested_lines[lineno] = line
    for lineno, line in ((c[1], c[2]) for c in changes if c[0] == 'add'):
        suggested_lines[lineno] = line

    logger.warning("Suggested diff for %s:\n%s", ''.join(
        difflib.unified_diff(lines, suggested_lines)
    ))


class X2ManyLinter(BaseCase):
    def test_x2many_lint(self):
        #for module in get_modules():
        for module in ['base', 'mail', 'stock']:
            if module in SKIP_MODULES:
                continue

            addon_path = pathlib.Path(get_module_path(module))
            print(addon_path)

            for file_ext in ('py', 'xml'):
                for path in addon_path.glob(f'**/*.{file_ext}'):
                    if str(path.relative_to(addon_path.parent)) in SKIP_FILES:
                        continue
                    with self.subTest(path=path):
                        x2many_lint(path, file_ext)
