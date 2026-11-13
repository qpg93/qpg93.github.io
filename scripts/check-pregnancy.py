#!/usr/bin/env python3
"""Validate the de-identified draft preview with Python's standard library.

Build outside the public output directory first:
  hugo --buildDrafts --destination /tmp/qpg93-baby-preview --minify --panicOnWarning
  python3 scripts/check-pregnancy.py /tmp/qpg93-baby-preview
This checks structure and values, not clinical correctness or browser behavior.
"""
import math
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/tmp/qpg93-baby-preview')
page = (root / 'baby/index.html').read_text()
source = Path('content/posts/baby.md').read_text()


class Charts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
        self.charts = []
        self.current = None
        self.diagrams = 0
        self.has_images = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = a.get('class', '').split()
        if a.get('id'):
            assert a['id'] not in self.ids, f'Duplicate id: {a["id"]}'
            self.ids.add(a['id'])
        self.references.extend(a.get('aria-labelledby', '').split())
        if tag == 'img':
            self.has_images = True
        if tag == 'figure' and 'data-chart' in classes:
            self.current = {'key': a['data-chart-key'], 'dots': 0, 'buttons': 0, 'tables': 0, 'lines': 0, 'values': [], 'labels': []}
            self.charts.append(self.current)
        if tag == 'figure' and 'pregnancy-diagram' in classes:
            self.diagrams += 1
        if self.current is not None:
            if 'chart-dot' in classes:
                x, y = float(a['cx']), float(a['cy'])
                assert math.isfinite(x) and math.isfinite(y)
                assert 72 <= x <= 640 and 42 <= y <= 250
                self.current['dots'] += 1
            if 'data-chart-point' in a:
                self.current['buttons'] += 1
                self.current['values'].append(a['data-value'])
                self.current['labels'].append(a['data-label'])
            if tag == 'table':
                self.current['tables'] += 1
            if 'chart-line' in classes:
                self.current['lines'] += 1
                assert 'NaN' not in a['points'] and 'Inf' not in a['points']

    def handle_endtag(self, tag):
        if tag == 'figure':
            self.current = None


parsed = Charts()
parsed.feed(page)
assert not parsed.has_images, 'Do not publish report images'
assert len(parsed.charts) == 9
assert parsed.diagrams == 2
expected = {
    'hcg': ['8988 mIU/mL', '20337 mIU/mL', '23226 mIU/mL', '39049 mIU/mL', '67225 mIU/mL'],
    'crl': ['2 mm', '5 mm', '8 mm', '32 mm', '65 mm'],
    'cervix': ['42 mm', '35 mm'],
    'bpd': ['38 mm', '50 mm', '55 mm', '62 mm'],
    'hc': ['130 mm', '177 mm', '200 mm', '234 mm'],
    'ac': ['116 mm', '161 mm', '173 mm', '213 mm'],
    'fl': ['22 mm', '34 mm', '38 mm', '47 mm'],
    'weight': ['About 385 g', 'About 486 g', '800–850 g (range; midpoint plotted)'],
    'ogtt': ['4.13 mmol/L', '6.74 mmol/L', '5.49 mmol/L'],
}
assert {c['key'] for c in parsed.charts} == set(expected)
for chart in parsed.charts:
    assert chart['values'] == expected[chart['key']], f'Data mismatch: {chart["key"]}'
    if chart['key'] in ('bpd', 'hc', 'ac', 'fl'):
        assert chart['labels'] == ['16w6d', '20w6d', '22w6d', '25w6d']
assert all(c['dots'] == c['buttons'] and c['dots'] >= 2 and c['tables'] == 1 and c['lines'] == 1 for c in parsed.charts)
assert all(ref in parsed.ids for ref in parsed.references)
assert 'ZgotmplZ' not in page and '<!-- raw HTML omitted -->' not in page
assert 'date: 2026-05-16' in source
assert 'title: "一起生长（持续更新）"' in source
assert re.search(r'^draft: (?:true|false)$', source, re.M)
assert 'subtitle:' not in source
assert 'Emma' in source and 'Yoyo' in source
assert not re.search(r'妈妈|妻子|\b\d{17}[\dXx]\b|(?<!\d)1[3-9]\d{9}(?!\d)|\d{1,3}\s*岁', source)
# Preserve the article date, but do not include calendar dates for visits.
assert not re.search(r'202[67][-年/]\d{1,2}[-月/]\d{1,2}', source.replace('date: 2026-05-16', ''))
for marker in ['800–850', '825', 'CHAT-BASED ESTIMATES', '宫颈', '116.25', '3353', '4.13', '6.74', '5.49']:
    assert marker in page, marker
assert 'https://www.nhs.uk/pregnancy/your-pregnancy-care/12-week-scan/' in page
assert 'https://www.nhs.uk/pregnancy/labour-and-birth/if-your-baby-is-breech/' in page
assert (root / 'js/charts.js').is_file() and (root / 'css/charts.css').is_file()
print('OK: 9 accessible SVG charts, 2 sourced diagrams, ranges, data tables and metadata/privacy guards')
