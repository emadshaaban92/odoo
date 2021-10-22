# pylint: skip-file
import csv
from collections import defaultdict
import os
from pathlib import Path
import re

from transform_tools import Field, Ref
from transform_models import Record



def load_old_csv(model):
    """
        Look for old Chart Template file and read it.
    """
    filenames = (
        f"{model}",
        f"{model}".replace('_', '.'),
        f"{model}_template",
        f"{model}_template".replace('_', '.'),
    )
    for name in filenames:
        paths = (
            list(Path.cwd().glob(f'addons/*/data/{name}.csv'))
            + list(Path.cwd().glob(f'addons/*/data/{name}-*.csv'))
        )
        for path in paths:
            module = str(path).split('/')[-3]
            if not module.startswith('l10n_'): continue
            with open(path, newline='', encoding='utf-8') as csvfile:
                yield module, csvfile
            os.remove(path)

def read_csv_lines(model):
    for module, csvfile in load_old_csv(model):
        csvcontent = (csvfile and csvfile.read() or '').split('\n')
        if not csvcontent:
            continue
        reader = csv.reader(csvcontent, delimiter=',')
        yield module, [line for line in reader if line]

def cleanup_csv(header, rows):
    for i, column in enumerate(header):
        if column in ('tag_ids', 'country_id'):
            column = column + '/id'
        header[i] = '"' + str(column).replace('"', '\\"') + '"'
        if column == 'id':
            id_column  = i
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            if value in ('TRUE', 'FALSE'):
                value = {'TRUE': True, 'FALSE': False}.get(value)
            if value is None:
                value = ""
            if j == id_column:
                value = value.split('.')[-1]
            rows[i][j] = '"' + str(value).replace('"', '\\"') + '"'
    return header, rows

def extract_template_column(header, rows, fields, remove=True):
    column = None
    templates = []
    for i, field in enumerate(header):
        if field in fields:
            column = i
        elif field.endswith(':id') or field.endswith('/id'):
            header[i] = header[i][:-3]
    if column is not None:
        getattr(header, 'pop' if remove else '__getitem__')(column)
        for row in rows:
            templates.append(getattr(row, 'pop' if remove else '__getitem__')(column))
    else:
        templates = [None] * len(rows)
    return header, rows, templates

def convert_records_to_csv(records, model):
    records = {
        **records.get(model, {}),
        **records.get(f"{model}.template", {})
    }
    rows = []
    header = list({
        _id.replace(":", "/"): True
        for record in records.values()
        for _id in record.get('children', {})
    })
    if 'id' not in header:
        header.insert(0, "id")
    for record in records.values():
        children = record.get('children', {})
        rows.append([
            record['id'] if field == 'id'
            else '' if field not in children
            else ','.join(
                str(s)[1:-1] if str(s).startswith("'") else str(s)
                for s in children[field]._value[0][2])
                if isinstance(children[field]._value, list
            )
            else children[field]._value
            for field in header
        ])
    header, rows = cleanup_csv(header, rows)
    if not header or not rows:
        return None
    return ('\n'.join(','.join([str(field) for field in row]) for row in [header] + rows)).strip()

def convert_csv_to_records(model):
    """
        Convert old CSV to Records, so that it can be further be processed.
        For example, it can be turned into a Python list.
    """
    records = defaultdict(dict)
    for module, lines in read_csv_lines(model):
        header, *rows = lines
        if model == 'account.chart.template':
            header, rows, templates = extract_template_column(header, rows, ('id',), remove=False)
        else:
            header, rows, templates = extract_template_column(header, rows, ('chart_template_id/id', 'chart_template_id:id'))
        id_idx = header.index('id')
        for i, (row, template) in enumerate(zip(rows, templates)):
            _id = row[id_idx]
            records[(module, template)][_id] = Record({'id': _id, 'tag': 'record', 'model': model}, 'record', module)
            for i, field_header in enumerate(header[:len(row)]):
                is_ref = re.match(r'^ref\(.*\)$', row[i], re.I)
                records[(module, template)][_id].append(Field({
                    'id': field_header,
                    'text': row[i] if not is_ref else '',
                    'ref': Ref(row[i]) if is_ref else ''
                }))
    return records
