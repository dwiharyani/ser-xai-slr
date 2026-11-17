"""Export public categorical coding matrices without private free-text reviewer notes.

Usage (local, with the original workbooks kept outside a public repository):
  python scripts/export_public_coder_tables.py FIRST_CODER.xlsx SECOND_CODER.xlsx

Only the first 19 coded and bibliographic columns are exported (through 'Eval: Automated
rationale scoring'). Evidence locators, reviewer remarks, priority-sample flags and notes
are excluded from the public files. Existing agreement JSON is not recomputed here.
"""
from pathlib import Path
import sys
from artifact_tool import Workbook, SpreadsheetFile, Blob

ROOT = Path(__file__).resolve().parents[1]
if len(sys.argv) != 3:
    raise SystemExit('Pass FIRST_CODER.xlsx and SECOND_CODER.xlsx as arguments')

def export(source, out_name, label):
    source = Path(source)
    wb = SpreadsheetFile.import_xlsx(Blob.load(str(source)))
    rows = wb.worksheets.get_item('Coding').get_range('A1:S80').values
    rows = [rows[0]] + [row for row in rows[1:] if isinstance(row[0], str) and row[0].startswith('M-')]
    assert len(rows) == 62 and len({row[0] for row in rows[1:]}) == 61
    # Remove the optional reviewer-selected 'Priority sample' field to avoid any tracking notes.
    public_columns = list(range(4)) + list(range(5,19))
    public = [[row[i] for i in public_columns] for row in rows]
    # Avoid false spreadsheet formula execution when workbook is opened.
    for row in public[1:]:
        for j, v in enumerate(row):
            if isinstance(v, str) and v.startswith(('=', '+', '-', '@')):
                row[j] = "'" + v
    out = Workbook.create()
    info = out.worksheets.add('About')
    info.get_range('A1:B5').values = [
        ['XAI-SER independent coding', label],
        ['Included studies', 61],
        ['Content', 'Initial categorical codes and bibliographic identifiers before adjudication'],
        ['Omitted', 'Evidence locators, free-text reviewer notes, priority sampling flags, personal commentary'],
        ['Scope', 'Public companion data: not a substitute for inspecting the full texts'],
    ]
    info.get_range('A1:A5').format = {'font': {'bold': True, 'color': '#355F3B'}, 'column_width': 26}
    info.get_range('B1:B5').format.column_width = 95
    info.get_range('B1:B5').format.wrap_text = True
    data = out.worksheets.add('Coding')
    data.get_range_by_indexes(0, 0, len(public), len(public[0])).values = public
    headers = data.get_range_by_indexes(0, 0, 1, len(public[0]))
    headers.format = {'fill': '#355F3B', 'font': {'bold': True, 'color': '#FFFFFF'}, 'wrap_text': True, 'row_height': 40}
    data.freeze_panes.freeze_rows(1)
    data.get_range('A:A').format.column_width = 13
    data.get_range('B:B').format.column_width = 10
    data.get_range('C:C').format.column_width = 55
    data.get_range('D:D').format.column_width = 34
    data.get_range('E:H').format.column_width = 29
    data.get_range('I:R').format.column_width = 24
    dest = ROOT / 'public' / 'downloads' / out_name
    SpreadsheetFile.export_xlsx(out).save(str(dest))
    print(label, len(public)-1, 'public codes ->', dest)
    return {str(row[0]) for row in rows[1:]}

first = export(sys.argv[1], 'XAI_SER_First_Coder_Coding_Public.xlsx', 'First coder (initial independent codes)')
second = export(sys.argv[2], 'XAI_SER_Second_Coder_Coding_Public.xlsx', 'Second coder (initial independent codes)')
assert first == second and len(first) == 61
