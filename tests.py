# Note: running this test suite successfully will generate the actual target outputs at the same time
# If the tests pass and a manual check that readme.md looks good, commit and push
import unittest
from export_books import ImportPratchett, ExportHTML, ExportMarkdown, MergeMarkDown, ExportCompactMarkdown
from export_books import Title

# input files
data_file = 'data.csv'
used_sprints_file = 'used.csv'
template_file = 'template.md'

# output files
merge_file = 'README.md'
html_file = 'index.html'
markdown_file = 'index.md'

class MatcherTests(unittest.TestCase):
    def test_strips_the(self):
        """ strips the prefix the when matching"""
        assert Title("The Wee Free Men") == Title("Wee Free Men")

    def test_subtitles(self):
        Title("A Blink of the Screen : collected short fiction") == Title("A Blink of the Screen ")

    def test_strip_a(self):
        """ strips a when matching """
        assert Title("A Hat Full of Sky") == Title("Hat Full of Sky")

    def test_removes_and(self):
        """ we strip '&' from the title, test and verify that removing 'and' will also get a match """
        assert Title("Johnny and the bomb") == Title("Johnny & the bomb")

    def test_removes_spaces(self):
        assert Title("Good Omens") == Title("Good  Omens")

    def test_case_sensitivity(self):
        assert Title("Moving pictures") == Title("Moving Pictures")

    def test_punctuation(self):
        assert Title("Guards Guards") == Title("Guards! Guards!")
        assert Title("Arbitrary") == Title("Arbitrary^")
        assert Title("wheres my cow") == Title("Where's my cow?")
        # hyphenation cases that we care about
        assert Title("reaper man") != Title("reaper-man")
        assert Title("ReaperMan") == Title("reaper-man")

class ImporterTests(unittest.TestCase):
    def test_import_csv(self):
        imp = ImportPratchett()
        csv = imp.import_csv(data_file)
        for row in csv:
            print(', '.join(row))
        assert(csv[0] == ['book','blurb','seq','class'])
        assert len(csv) > 10

    def test_import_used_sprints(self):
        """
        if used_sprints_file is none, ignore this test
        """
        if used_sprints_file:
            importer = ImportPratchett()
            used = importer.import_csv(used_sprints_file)
            assert (used[0] == ['book'])
            used = used[1::]
            used = [Title(item) for sublist in used for item in sublist]

            csv = importer.import_csv(data_file)
            csv = csv[1::]
            for row in csv:
                if Title(row[0]) in used:
                    print("U {}".format(row[0]))
                else:
                    print("F {}".format(row[0]))

    def test_merge_used_sprints(self):
        if used_sprints_file:
            importer = ImportPratchett()
            used = importer.import_csv(used_sprints_file)
            assert (used[0] == ['book'])
            used = used[1::]
            used = [Title(item) for sublist in used for item in sublist]

            csv = importer.import_csv(data_file)
            csv_data = csv[1::]
            table_unused_books = [csv[0]]
            table_used_books = table_unused_books[:]
            for row in csv_data:
                if Title(row[0]) in used:
                    print("U {}".format(row[0]))
                    table_used_books.append(row)
                else:
                    print("F {}".format(row[0]))
                    table_unused_books.append(row)

            md = ExportCompactMarkdown()
            used_text = md.export_mark_down(table_used_books, ['Used Titles'])
            unused_text = md.export_mark_down(table_unused_books, ['Remaining Titles'])
            with open(template_file) as f:
                template = f.readlines()
            text = unused_text + "\r\n\r\n" + used_text
            transformed = "".join(template).replace("<TABLE>", text)
            generated = transformed.replace("<GENERATED>", "Note: This file was generated from {}".format(template_file))
            md.save_text(generated, merge_file)  # readme.md


class ExporterTests(unittest.TestCase):
    def test_export_html(self):
        imp = ImportPratchett()
        csv = imp.import_csv(data_file)
        html = ExportHTML(csv).getvalue()
        assert len(html)
        # export again, but the short form with just links
        html = ExportHTML()
        text = html.export_html(csv, ['Title'])
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
        merge_file_name = merge_file
        if used_sprints_file:
            merge_file_name += ".1"
        md.save_text(generated, merge_file_name)  # readme.md


if __name__ == '__main__':
    unittest.main()
