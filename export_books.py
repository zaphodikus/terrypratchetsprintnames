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

class ExportHTML(object):
    def __init__(self, books):
        self._books = books

    def getvalue(self):
        return self.export_html(self._books, headings=["Title","Link","Hash","Book type"])

    @staticmethod
    def save_html(text, filename):
        with open(filename, "w") as f:
            f.write(text)

    def export_html(self, books, headings):
        html = """<html><table border="1">
"""
        def makeheading(row, indent=2):
            h = "{}<tr>".format(' '*indent)
            for item in row:
                h+= "<th>{}</th>".format(item)
            h+= "\n{}</tr>".format(' '*indent)
            return h

        def makerow(row, indent=2):
            h=  "{}<tr>".format(' '*indent)
            for item in row:
                h+= "<td>{}</td>".format(item)
            h+= "\n{}</tr>".format(' '*indent)
            return h

        head = None
        for row in books:
            if head:
                html += makerow(row)
            else:
                head = makeheading(headings)
                html += head
        html += "</table></html>"
        return html

class ExportMarkdown(object):
    pass

class MergeMarkDown(object):
    pass