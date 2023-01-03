# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Modified html2text v.3.200.3 Aaron Swartz (me@aaronsw.com) under GNU GPL 3.
# Original version: https://github.com/aaronsw/html2text/blob/master/html2text.py
# A part from
# * PEP8 styling and whitespace changes throughout the code
# * removing support for Google doc
# * removing support for non Py3 code
# changes from the original version are surrounded by [changes] and [/changes] comment tags.


# [changes] Simplify imports to python 3 only
from html import entities as html_entity_defs
import html.parser as html_parser
import re
import urllib.parse as urlparse
from textwrap import wrap
# [/changes]

# Use Unicode characters instead of their ascii psuedo-replacements
UNICODE_SNOB = 0

# Escape all special characters.  Output is less readable, but avoids corner case formatting issues.
ESCAPE_SNOB = False  # [change] 0 to False

# Put the links after each paragraph instead of at the end.
LINKS_EACH_PARAGRAPH = 0

# Wrap long lines at position. 0 for no wrapping.
BODY_WIDTH = 78

# Don't show internal links (href="#local-anchor") -- corresponding link targets
# won't be visible in the plain text file anyway.
SKIP_INTERNAL_LINKS = True

# Use inline, rather than reference, formatting for images and links
INLINE_LINKS = True

IGNORE_ANCHORS = False
IGNORE_IMAGES = False
IGNORE_EMPHASIS = False

# [changes] additional constant values renamed and moved here
R_UNESCAPE = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")

# [/changes]


# [changes] Move here from bottom, update name, signature and usage
def _html2plaintext(html):
    h = HTML2Text()
    return h.handle(html)


# ### Entity Nonsense ###
def name2cp(k):
    if k == 'apos':
        return ord("'")
    return html_entity_defs.name2codepoint[k]


unifiable = {'rsquo': "'", 'lsquo': "'", 'rdquo': '"', 'ldquo': '"',
             'copy': '(C)', 'mdash': '--', 'nbsp': ' ', 'rarr': '->', 'larr': '<-', 'middot': '*',
             'ndash': '-', 'oelig': 'oe', 'aelig': 'ae',
             'agrave': 'a', 'aacute': 'a', 'acirc': 'a', 'atilde': 'a', 'auml': 'a', 'aring': 'a',
             'egrave': 'e', 'eacute': 'e', 'ecirc': 'e', 'euml': 'e',
             'igrave': 'i', 'iacute': 'i', 'icirc': 'i', 'iuml': 'i',
             'ograve': 'o', 'oacute': 'o', 'ocirc': 'o', 'otilde': 'o', 'ouml': 'o',
             'ugrave': 'u', 'uacute': 'u', 'ucirc': 'u', 'uuml': 'u',
             'lrm': '', 'rlm': ''}

# [Changes] simplification with Py3 [/changes]
unifiable_n = {name2cp(k): v for k, v in unifiable.items()}

# ### End Entity Nonsense ###


def onlywhite(line):
    """Return true if the line does only consist of whitespace characters."""
    for c in line:
        if c != ' ' and c != '  ':
            return c == ' '
    return line


def hn(tag):
    if tag[0] == 'h' and len(tag) == 2:
        try:
            n = int(tag[1])
            if n in range(1, 10):
                return n
        except ValueError:
            return 0


def dumb_property_dict(style):
    """returns a hash of css attributes"""
    return dict([(x.strip(), y.strip()) for x, y in [z.split(':', 1) for z in style.split(';') if ':' in z]])


def dumb_css_parser(data):
    """returns a hash of css selectors, each of which contains a hash of css attributes"""
    # remove @import sentences
    data += ';'
    import_index = data.find('@import')
    while import_index != -1:
        data = data[0:import_index] + data[data.find(';', import_index) + 1:]
        import_index = data.find('@import')

    # parse the css. reverted from dictionary compehension in order to support older pythons
    elements = [x.split('{') for x in data.split('}') if '{' in x.strip()]
    try:
        elements = dict([(a.strip(), dumb_property_dict(b)) for a, b in elements])
    except ValueError:
        elements = {}  # not that important

    return elements


def element_style(attrs, style_def, parent_style):
    """returns a hash of the 'final' style attributes of the element"""
    style = parent_style.copy()
    if 'class' in attrs:
        for css_class in attrs['class'].split():
            css_style = style_def['.' + css_class]
            style.update(css_style)
    if 'style' in attrs:
        immediate_style = dumb_property_dict(attrs['style'])
        style.update(immediate_style)
    return style


def list_numbering_start(attrs):
    """extract numbering from list element attributes"""
    if 'start' in attrs:
        return int(attrs['start']) - 1
    else:
        return 0


class HTML2Text(html_parser.HTMLParser):
    def __init__(self, out=None, baseurl=''):
        html_parser.HTMLParser.__init__(self)

        # Config options
        self.unicode_snob = UNICODE_SNOB
        self.escape_snob = ESCAPE_SNOB
        self.links_each_paragraph = LINKS_EACH_PARAGRAPH
        self.body_width = BODY_WIDTH
        self.skip_internal_links = SKIP_INTERNAL_LINKS
        self.inline_links = INLINE_LINKS
        self.ignore_links = IGNORE_ANCHORS
        self.ignore_images = IGNORE_IMAGES
        self.ignore_emphasis = IGNORE_EMPHASIS
        self.ul_item_mark = '*'
        self.emphasis_mark = '_'
        self.strong_mark = '**'
        self.hr_markdown = "* * *"

        if out is None:
            self.out = self.out_text_f
        else:
            self.out = out

        self.out_text_list = []  # empty list to store output characters before they are "joined"

        self.out_text = str()

        self.quiet = 0
        self.p_p = 0  # number of newline character to print before next output
        self.out_count = 0
        self.start = True
        self.space = 0
        self.a = []
        self.astack = []
        self.maybe_automatic_link = None
        self.absolute_url_matcher = re.compile(r'^[a-zA-Z+]+://')
        self.a_count = 0
        self.list = []
        self.blockquote = 0
        self.pre = 0
        self.start_pre = 0
        self.code = False
        self.br_toggle = ''
        self.lastWasNL = 0
        self.lastWasList = False
        self.style = 0
        self.style_def = {}
        self.tag_stack = []
        self.emphasis = 0
        self.drop_white_space = 0
        self.in_header = False
        self.abbr_title = None  # current abbreviation definition
        self.abbr_data = None  # last inner HTML (for abbr being defined)
        self.abbr_list = {}  # stack of abbreviations to write later
        self.baseurl = baseurl

        unifiable_n.pop(name2cp('nbsp'), None)
        unifiable['nbsp'] = '&nbsp_place_holder;'

    def feed(self, data):
        data = data.replace("</' + 'script>", "</ignore>")
        html_parser.HTMLParser.feed(self, data)

    def handle(self, data):
        self.feed(data)
        self.feed("")
        return self.optwrap(self.close())

    def out_text_f(self, s):
        self.out_text_list.append(s)
        if s:
            self.lastWasNL = s[-1] == '\n'

    def close(self):
        """:rtype: str"""
        html_parser.HTMLParser.close(self)

        self.pbr()
        self.o('', False, 'end')

        self.out_text = self.out_text.join(self.out_text_list)
        if self.unicode_snob:
            nbsp = chr(name2cp('nbsp'))
        else:
            nbsp = u' '
        self.out_text = self.out_text.replace(u'&nbsp_place_holder;', nbsp)

        return self.out_text

    def handle_charref(self, c):
        self.o(self.charref(c), True)

    def handle_entityref(self, c):
        self.o(self.entityref(c), True)

    def handle_starttag(self, tag, attrs):
        self.handle_tag(tag, attrs, 1)

    def handle_endtag(self, tag):
        self.handle_tag(tag, None, 0)

    def previous_index(self, attrs):
        """ returns the index of certain set of attributes (of a link) in the
            self.a list
            If the set of attributes is not found, returns None
        """
        # [changes] `in` replaces of `has_key` + styling + "match" simplification
        if 'href' not in attrs:
            return None

        i = -1
        for a in self.a:
            i += 1

            if 'href' in a and a['href'] == attrs['href']:
                if 'title' not in a and 'title' not in attrs:
                    return i
                if 'title' in a and 'title' in attrs and a['title'] == attrs['title']:
                    return i
        # [/changes]

    def drop_last(self, nb_letters):
        if not self.quiet:
            self.out_text = self.out_text[:-nb_letters]

    def handle_tag(self, tag, attrs, start):
        if attrs is None:
            attrs = {}
        else:
            attrs = dict(attrs)

        if hn(tag):
            self.p()
            if start:
                self.in_header = True
                self.o(hn(tag) * "#" + ' ')
            else:
                self.in_header = False
                return  # prevent redundant emphasis marks on headers

        if tag in ['p', 'div']:
            self.p()

        if tag == "br" and start:
            self.o("  \n")

        if tag == "hr" and start:
            self.p()
            self.o(self.hr_markdown)
            self.p()

        if tag in ["head", "style", 'script']:
            self.quiet += 1 if start else -1  # [change] use 'ternary' assignment

        if tag == "style":
            self.style += 1 if start else -1  # [change] use 'ternary' assignment

        if tag in ["body"]:
            self.quiet = 0  # sites like 9rules.com never close <head>

        if tag == "blockquote":
            if start:
                self.p()
                self.o('> ', pure_data=False, force=True)
                self.start = 1
                self.blockquote += 1
            else:
                self.blockquote -= 1
                self.p()

        if tag in ['em', 'i', 'u'] and not self.ignore_emphasis:
            self.o(self.emphasis_mark)
        if tag in ['strong', 'b'] and not self.ignore_emphasis:
            self.o(self.strong_mark)
        if tag in ['del', 'strike', 's']:
            if start:
                self.o("<" + tag + ">")
            else:
                self.o("</" + tag + ">")

        if tag in ["code", "tt"] and not self.pre:
            self.o('`')  # TODO: `` `this` ``
        if tag == "abbr":
            if start:
                self.abbr_title = None
                self.abbr_data = ''
                if 'title' in attrs:
                    self.abbr_title = attrs['title']
            else:
                if self.abbr_title is not None:
                    self.abbr_list[self.abbr_data] = self.abbr_title
                    self.abbr_title = None
                self.abbr_data = ''

        if tag == "a" and not self.ignore_links:
            if start:
                if 'href' in attrs and not (self.skip_internal_links and attrs['href'].startswith('#')):
                    self.astack.append(attrs)
                    self.maybe_automatic_link = attrs['href']
                else:
                    self.astack.append(None)
            else:
                if self.astack:
                    a = self.astack.pop()
                    if self.maybe_automatic_link:
                        self.maybe_automatic_link = None
                    elif a:
                        if self.inline_links:
                            self.o("](" + _escape_md(a['href']) + ")")
                        else:
                            i = self.previous_index(a)
                            if i is not None:
                                a = self.a[i]
                            else:
                                self.a_count += 1
                                a['count'] = self.a_count
                                a['out_count'] = self.out_count
                                self.a.append(a)
                            self.o("][" + str(a['count']) + "]")

        if tag == "img" and start and not self.ignore_images:
            if 'src' in attrs:
                attrs['href'] = attrs['src']
                alt = attrs.get('alt', '')
                self.o("![" + _escape_md(alt) + "]")

                if self.inline_links:
                    self.o("(" + _escape_md(attrs['href']) + ")")
                else:
                    i = self.previous_index(attrs)
                    if i is not None:
                        attrs = self.a[i]
                    else:
                        self.a_count += 1
                        attrs['count'] = self.a_count
                        attrs['out_count'] = self.out_count
                        self.a.append(attrs)
                    self.o("[" + str(attrs['count']) + "]")

        if tag == 'dl' and start:
            self.p()
        if tag == 'dt' and not start:
            self.pbr()
        if tag == 'dd' and start:
            self.o('    ')
        if tag == 'dd' and not start:
            self.pbr()

        if tag in ["ol", "ul"]:
            # Google Docs create sub lists as top level lists  # odoo: kept as may be the case of any code
            if (not self.list) and (not self.lastWasList):
                self.p()
            if start:
                list_style = tag
                numbering_start = list_numbering_start(attrs)
                self.list.append({'name': list_style, 'num': numbering_start})
            else:
                if self.list:
                    self.list.pop()
            self.lastWasList = True
        else:
            self.lastWasList = False

        if tag == 'li':
            self.pbr()
            if start:
                if self.list:
                    li = self.list[-1]
                else:
                    li = {'name': 'ul', 'num': 0}
                nest_count = len(self.list)
                self.o("  " * nest_count)  # TODO: line up <ol><li>s > 9 correctly.
                if li['name'] == "ul":
                    self.o(self.ul_item_mark + " ")
                elif li['name'] == "ol":
                    li['num'] += 1
                    self.o(str(li['num']) + ". ")
                self.start = 1

        if tag in ["table", "tr"] and start:
            self.p()
        if tag == 'td':
            self.pbr()

        if tag == "pre":
            if start:
                self.start_pre = 1
                self.pre = 1
            else:
                self.pre = 0
            self.p()

    def pbr(self):
        if self.p_p == 0:
            self.p_p = 1

    def p(self):
        self.p_p = 2

    def soft_br(self):
        self.pbr()
        self.br_toggle = '  '

    # [changes] flags to `bool`
    def o(self, data, pure_data=False, force=False):
        """
        :param data:
        :param bool pure_data:
        :param bool|str force:
        """
        if self.abbr_data is not None:
            self.abbr_data += data

        if not self.quiet:
            if pure_data and not self.pre:
                data = re.sub(r'\s+', ' ', data)  # [changes] use of r string
                if data and data[0] == ' ':
                    self.space = 1
                    data = data[1:]
            if not data and not force:
                return

            if self.start_pre:
                # self.out(" :") #TODO: not output when already one there
                if not data.startswith("\n"):  # <pre>stuff...
                    data = "\n" + data

            bq = (">" * self.blockquote)
            if not (force and data and data[0] == ">") and self.blockquote:
                bq += " "

            if self.pre:
                if not self.list:
                    bq += "    "
                # else: list content is already partially indented
                for i in range(len(self.list)):  # [changes] Py3 range
                    bq += "    "
                data = data.replace("\n", "\n" + bq)

            if self.start_pre:
                self.start_pre = 0
                if self.list:
                    data = data.lstrip("\n")  # use existing initial indentation

            if self.start:
                self.space = 0
                self.p_p = 0
                self.start = False

            if force == 'end':
                # It's the end.
                self.p_p = 0
                self.out("\n")
                self.space = 0

            if self.p_p:
                self.out((self.br_toggle + '\n' + bq) * self.p_p)
                self.space = 0
                self.br_toggle = ''

            if self.space:
                if not self.lastWasNL:
                    self.out(' ')
                self.space = 0

            if self.a and ((self.p_p == 2 and self.links_each_paragraph) or force == "end"):
                if force == "end":
                    self.out("\n")

                new_a = []
                for link in self.a:
                    if self.out_count > link['out_count']:
                        self.out("   [" + str(link['count']) + "]: " + urlparse.urljoin(self.baseurl, link['href']))
                        # [changes] `has_key` => `in`
                        if 'title' in link:
                            self.out(" (" + link['title'] + ")")
                        self.out("\n")
                    else:
                        new_a.append(link)

                if self.a != new_a:
                    self.out("\n")  # Don't need an extra line when nothing was done.

                self.a = new_a

            if self.abbr_list and force == "end":
                for abbr, definition in self.abbr_list.items():
                    self.out("  *[" + abbr + "]: " + definition + "\n")

            self.p_p = 0
            self.out(data)
            self.out_count += 1

    def handle_data(self, data):
        if r'\/script>' in data:
            self.quiet -= 1

        if self.style:
            self.style_def.update(dumb_css_parser(data))

        if self.maybe_automatic_link is not None:
            href = self.maybe_automatic_link
            if href == data and self.absolute_url_matcher.match(href):
                self.o("<" + data + ">")
                return
            else:
                self.o("[")
                self.maybe_automatic_link = None

        if not self.code and not self.pre:
            data = _escape_md_section(data, snob=self.escape_snob)
        self.o(data, True)

    def unknown_decl(self, data):
        pass

    def charref(self, name):
        if name[0] in ['x', 'X']:
            c = int(name[1:], 16)
        else:
            c = int(name)

        if not self.unicode_snob and c in unifiable_n.keys():
            return unifiable_n[c]

        return chr(c)

    def entityref(self, c):
        if not self.unicode_snob and c in unifiable.keys():
            return unifiable[c]
        try:
            return chr(name2cp(c))
        except KeyError:
            return "&" + c + ';'

    def replace_entities(self, s):
        s = s.group(1)
        if s[0] == "#":
            return self.charref(s[1:])
        else:
            return self.entityref(s)

    def unescape(self, s):
        return R_UNESCAPE.sub(self.replace_entities, s)

    def optwrap(self, text):
        """Wrap all paragraphs in the provided text."""
        if not self.body_width:
            return text

        result = ''
        newlines = 0
        for para in text.split("\n"):
            if len(para) > 0:
                if not skip_wrap(para):
                    result += "\n".join(wrap(para, self.body_width))
                    if para.endswith('  '):
                        result += "  \n"
                        newlines = 1
                    else:
                        result += "\n\n"
                        newlines = 2
                else:
                    if not onlywhite(para):
                        result += para + "\n"
                        newlines = 1
            else:
                if newlines < 2:
                    result += "\n"
                    newlines += 1
        return result


ordered_list_matcher = re.compile(r'\d+\.\s')
unordered_list_matcher = re.compile(r'[-*+]\s')  # [changes] remove redundant `\`
md_chars_matcher = re.compile(r"([\\\[\]()])")  # [changes] remove redundant `\`
md_chars_matcher_all = re.compile(r"([`*_{}\[\]()#!])")  # [changes] remove redundant `\`
md_dot_matcher = re.compile(r"""
    ^             # start of line
    (\s*\d+)      # optional whitespace and a number
    (\.)          # dot
    (?=\s)        # lookahead assert whitespace
    """, re.MULTILINE | re.VERBOSE)
md_plus_matcher = re.compile(r"""
    ^
    (\s*)
    (\+)
    (?=\s)
    """, flags=re.MULTILINE | re.VERBOSE)
# [changes] remove dash escape [/changes]

slash_chars = r'\`*_{}[]()#+-.!'
md_backslash_matcher = re.compile(r'''
    (\\)          # match one slash
    (?=[%s])      # followed by a char that requires escaping
    ''' % re.escape(slash_chars),
                                  flags=re.VERBOSE)


def skip_wrap(para):
    # If the text begins with four spaces or one tab, it's a code block; don't wrap
    if para[0:4] == '    ' or para[0] == '\t':
        return True
    # If the text begins with only two "--", possibly preceded by whitespace, that's
    # an emdash; so wrap.
    stripped = para.lstrip()
    if stripped[0:2] == "--" and len(stripped) > 2 and stripped[2] != "-":
        return False
    # I'm not sure what this is for; I thought it was to detect lists, but there's
    # a <br>-inside-<span> case in one of the tests that also depends upon it.
    if stripped[0:1] == '-' or stripped[0:1] == '*':
        return True
    # If the text begins with a single -, *, or +, followed by a space, or an integer,
    # followed by a ., followed by a space (in either case optionally preceeded by
    # whitespace), it's a list; don't wrap.
    if ordered_list_matcher.match(stripped) or unordered_list_matcher.match(stripped):
        return True
    return False


# [changes] remove unused commands [/changes]
def _escape_md(text):
    """Escapes markdown-sensitive characters within other markdown constructs."""
    return md_chars_matcher.sub(r"\\\1", text)


def _escape_md_section(text, snob=False):
    """Escapes markdown-sensitive characters across whole document sections."""
    text = md_backslash_matcher.sub(r"\\\1", text)
    if snob:
        text = md_chars_matcher_all.sub(r"\\\1", text)
    text = md_dot_matcher.sub(r"\1\\\2", text)
    text = md_plus_matcher.sub(r"\1\\\2", text)
    # [changes] Remove dash escape [/changes]
    return text
