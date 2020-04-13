# generate a human readable list of pratchet books based on a CSV file
# 1. An HTML listing
# 2. A .MD markdown listing
# 3. Merge markdown file with README.MD
import csv


class ImportPratchett(object):

    def import_csv(self, file):
        result = []
        with open(file, 'r') as csvfile:
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

    def getvalue(self):
        return self.export_html(self._books, headings=["Title","Link","Hash","Book type"])

    @staticmethod
    def _rowrender(row, indent =2):
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
        def makeheading(row, indent=2):
            h = "{}<tr>".format(' '*indent)
            for item in row:
                h+= "<th>{}</th>".format(item)
            h+= "\n{}</tr>".format(' '*indent)
            return h

        def makerow(row, rowrender, indent=2):
            if callable(rowrender):
                return rowrender(row)
            else:
                return rowrender.__func__(row)


        head = None
        for row in books:
            if head:
                html += makerow(row, rowrender)
            else:
                head = makeheading(headings)
                html += head
        html += "</table></html>"
        return html


class ExportMarkdown(TextSaver):
    def __init__(self, books):
        self._books = books

    def getvalue(self):
        return self.export_mark_down(self._books, headings=["Title", "Link", "Hash", "Book type"])

    @staticmethod
    def save_text(text, filename):
        with open(filename, "w") as f:
            f.write(text)


    def makerow(self, row):
        r = "|"
        for item in row:
            r += " {} |".format(item)
        r += "\n"
        return r

    def makeheading(self, row):
        h = "\n"
        h += self.makerow(row)
        for item in row:
            h += "| --- "
        h += "|\n"
        return h

    def export_mark_down(self, books, headings):
        mark_down = """##H2 Books
    """

        mark_down = None
        for row in books:
            if mark_down:
                mark_down += self.makerow(row)
            else:
                mark_down = self.makeheading(headings)
        return mark_down

class ExportCompactMarkdown(ExportMarkdown):
    def __init__(self):
        self._books = None

    def getvalue(self):
        pass # do not call!

    def makerow(self,row):
        """ All we do is redefine the row helpers
        """
        r = "| [{}]({}) |\n".format(row[0], row[1])
        return r

    def makeheading(self, head):
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