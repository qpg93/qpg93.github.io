#!/usr/bin/env python3
"""Check Hugo output using Python's standard library only."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path('public')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.links = []
        self.h1_count = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id in {self.path}'
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1_count += 1
        if tag in ('a', 'link', 'script', 'img'):
            url = attrs.get('href') if tag in ('a', 'link') else attrs.get('src')
            if url:
                self.links.append(url)


def resolve(path):
    target = ROOT / unquote(path).lstrip('/')
    return target / 'index.html' if target.is_dir() else target


required = ['index.html', 'init/index.html', 'about/index.html',
            'tags/index.html', 'tags/notice/index.html', '404.html',
            'feed.xml', 'sitemap.xml', 'search.json', 'robots.txt',
            'images/favicon.ico', 'archives/ysc.json', 'css/style.css', 'js/site.js']
for name in required:
    assert (ROOT / name).is_file(), f'Missing output: {name}'

pages = {path: Page(path) for path in ROOT.rglob('*.html')}
for path, page in pages.items():
    # Hugo's redirect aliases have no article heading.
    if '/page/' not in path.as_posix():
        assert page.h1_count == 1, f'Expected one H1: {path}'
    for url in page.links:
        parsed = urlsplit(url)
        if parsed.scheme and parsed.scheme not in ('http', 'https'):
            continue
        if parsed.netloc and parsed.netloc != 'qpg93.github.io':
            continue
        target = resolve(parsed.path) if parsed.path.startswith('/') else (
            path if not parsed.path else path.parent / unquote(parsed.path)
        )
        assert target.exists(), f'Broken link in {path}: {url}'
        if parsed.fragment and target in pages:
            assert unquote(parsed.fragment) in pages[target].ids, f'Broken anchor: {url}'

posts = json.loads((ROOT / 'search.json').read_text())
assert isinstance(posts, list)
assert len({p['url'] for p in posts}) == len(posts), 'Duplicate post URLs'
post = next(p for p in posts if p['url'] == '/init/')
assert post['date'] == '2024-10-09'
assert '在此记录想记录的一切。' in post['content']
assert post['tags'] == ['notice']
assert all(p['url'] != '/about/' for p in posts)
assert 'notice' in pages[ROOT / 'tags/index.html'].ids
assert "qpg93's personal blog" in (ROOT / 'index.html').read_text()
# Interface copy must remain English; Chinese is allowed in post content.
for folder, pattern in [('layouts', '*.html'), ('static/js', '*.js')]:
    for source in Path(folder).rglob(pattern):
        assert not re.search(r'[\u3400-\u4dbf\u4e00-\u9fff]', source.read_text()), f'Non-English UI copy: {source}'
for name in ['about/index.html', '404.html']:
    page = (ROOT / name).read_text()
    assert not re.search(r'[\u3400-\u4dbf\u4e00-\u9fff]', page), f'Non-English page: {name}'
for path in pages:
    assert re.search(r'<html\b[^>]*\blang=[\"\']?en(?:-[A-Za-z]+)?(?:[\"\'\s>])', path.read_text()), f'Expected English document: {path}'
for name in ['feed.xml', 'sitemap.xml']:
    ET.parse(ROOT / name)
print(f'OK: {len(pages)} HTML pages, local links, anchors, original post, search index, RSS and sitemap')
