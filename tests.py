# Note: running this test suite successfully will generate the actual target outputs at the same time
# If the tests pass and a manual check that readme.md looks good, commit and push
import unittest
from export_books import ImportPratchett, ExportHTML, ExportMarkdown, MergeMarkDown, ExportCompactMarkdown

data_file = 'data.csv'
html_file = 'index.html'
markdown_file = 'index.md'
template_file = 'template.md'
merge_file = 'README.md'

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
        # export again, but the short form with just links
        html = ExportHTML()
        text = html.export_html(csv, ['Title'], ExportHTML._compactrender)
        # save to file
        ExportHTML.save_text(text, html_file)

    def test_export_markdown(self):
        imp = ImportPratchett()
        csv = imp.import_csv(data_file)
        md = ExportMarkdown(csv).getvalue()
        assert len(md)
        md = ExportCompactMarkdown()
        text = md.export_mark_down(csv, ['Title'])
        # save
        md.save_text(text, markdown_file)

class MergeTests(unittest.TestCase):
    def test_merge(self):
        imp = ImportPratchett()
        csv = imp.import_csv(data_file)
        md = ExportCompactMarkdown()
        text = md.export_mark_down(csv, ['Title'])
        with open(template_file) as f:
            template = f.readlines()
        transformed = "".join(template).replace("<TABLE>", text)
        generated = transformed.replace("<GENERATED>", "Note: This file was generated from {}".format(template_file))
        md.save_text(generated, merge_file)  # readme.md


if __name__ == '__main__':
    unittest.main()
