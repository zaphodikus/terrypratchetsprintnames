# generate a human readable list of pratchet books based on a CSV file
# 1. An HTML listing
# 2. A .MD markdown listing
# 3. Merge markdown file with README.MD
import csv
import codecs
import os
import chardet


class Title:
    """
    helper class to compare book titles for equality
    """
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return self.item

    def clean(self):
        cleaned = self.item.lower().split(":")[0]
        for r in ",?^!":
            cleaned = cleaned.replace(r, "")
        return cleaned.strip()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.clean() == other.clean()
        else:  # assume, a normal string
            return self.clean() == Title(other).clean()

    def __ne__(self, other):
        return not self.__eq__(other)


class ImportPratchett(object):

    @staticmethod
    def encoding(filename):
        """ returns the best encoding to use when opening a file """
        bytes = min(32, os.path.getsize(filename))
        raw = open(filename, 'rb').read(bytes)

        if raw.startswith(codecs.BOM_UTF8):
            encoding = 'utf-8-sig'
        else:
            result = chardet.detect(raw)
            encoding = result['encoding']
        return encoding

    def import_csv(self, file):
        result = []

        enc = ImportPratchett.encoding(file)
        with codecs.open(file, 'r', enc) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvreader:
                result.append(row)
        return result


class TextSaver(object):
    @staticmethod
    def save_text(text, filename):
        with open(filename, "w") as f:
            f.write(text)


class ExportHTML(TextSaver):
    def __init__(self, books= None):
        self._books = books

    def getvalue(self, headings=["Title", "Link", "Hash", "Book type"]):
        return self.export_html(self._books, headings)

    @staticmethod
    def _rowrender(row, indent=2):
        """ By default use 4 headings in the table
        """
        h = "{}<tr>".format(' ' * indent)
        for item in row:
            h += "<td>{}</td>".format(item)
        h += "\n{}</tr>".format(' ' * indent)
        return h

    @staticmethod
    def _compactrender(row):
        """ Tiny table with title and URL combined"""
        h = "<tr><td><a href=""{}"">{}</a></td></tr>\n".format(row[1], row[0])
        return h

    def export_html(self, books, headings, rowrender=_rowrender):
        html = """<html><table border="1">
"""
        def make_heading(row, indent=2):
            h = "{}<tr>".format(' '*indent)
            for item in row:
                h+= "<th>{}</th>".format(item)
            h+= "\n{}</tr>".format(' '*indent)
            return h

        def make_row(row, rowrender, indent=2):
            if callable(rowrender):
                return rowrender(row)
            else:
                return rowrender.__func__(row)

        head = None
        for row in books:
            if head:
                html += make_row(row, rowrender)
            else:
                head = make_heading(headings)
                html += head
        html += "</table></html>"
        return html


class ExportMarkdown(TextSaver):
    def __init__(self, books):
        self._books = books

    def getvalue(self):
        return self.export_mark_down(self._books, headings=["Title", "Link", "Hash", "Book type"])

    def make_row(self, row):
        r = "|"
        for item in row:
            r += " {} |".format(item)
        r += "\n"
        return r

    def make_heading(self, row):
        h = "\n"
        h += self.make_row(row)
        for item in row:
            h += "| --- "
        h += "|\n"
        return h

    def export_mark_down(self, books, headings):
        mark_down = None
        for row in books:
            if mark_down:
                mark_down += self.make_row(row)
            else:
                mark_down = self.make_heading(headings)
        return mark_down


class ExportCompactMarkdown(ExportMarkdown):
    def __init__(self):
        self._books = None

    def getvalue(self):
        pass # do not call!

    def make_row(self, row):
        """ All we do is redefine the row helpers
        """
        r = "| [{}]({}) |\n".format(row[0], row[1])
        return r

    def make_heading(self, head):
        h = "\n|"
        for item in head:
            h += " {} |".format(item)
        h += "\n"
        for item in head:
            h += "| --- "
        h += "|\n"
        return h


class MergeMarkDown(object):
    pass
