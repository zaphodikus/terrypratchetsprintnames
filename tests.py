# note: running this test suite successfully will generate the actual target outputs at the same time
import unittest
from export_books import ImportPratchett, ExportHTML, ExportMarkdown, MergeMarkDown

data_file = 'data.csv'
html_file = 'index.html'
markdown_file = 'index.md'
merge_file = 'readme.md'

class ImporterTests(unittest.TestCase):
    def test_import_csv(self):
        imp = ImportPratchett()
        csv = imp.import_csv(data_file)
        for row in csv:
            print(', '.join(row))
        assert(csv[0] == ['book','blurb','seq','class'])
        assert len(csv) > 10

class ExporterTests(unittest.TestCase):
    def test_export_html(self):
        imp = ImportPratchett()
        csv = imp.import_csv(data_file)
        html = ExportHTML(csv).getvalue()
        assert len(html)
        ExportHTML.save_html(ExportHTML(csv).getvalue(), html_file)

    def test_export_markdown(self):
        self.assertEqual(True, False)

class MergeTests(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
