#!/usr/bin/env python3
"""Rebuild the offline app from the latest "My Italian words" page and a fresh data snapshot.

Usage: python3 rebuild.py PAGE.html SEED_DIR
  PAGE.html  the artifact page source (as published on claude.ai)
  SEED_DIR   folder with database docs saved as <collection>/<doc>.json
The offline parts (home-screen tags, the local database stand-in, the results box) are taken
from the current index.html, so they don't need to live anywhere else.
"""
import datetime, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
page_path, seed_dir = sys.argv[1], sys.argv[2]
version = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M')

old = open(os.path.join(HERE, 'index.html')).read()
t = '<title>Italiano offline</title>\n'
i = old.index(t) + len(t)
head = old[i:old.index('</style>\n', i) + len('</style>\n')]
j = old.index('<script>\n// Offline home-screen version')
offline_js = old[j:old.index('</script>\n', j) + len('</script>\n')]
offline_js = re.sub(r"var APP_VERSION = '\d+';", "var APP_VERSION = '%s';" % version, offline_js)

page = open(page_path).read()
assert '<title>My Italian words</title>' in page and page.count('<script>') == 1
page = page.replace('<title>My Italian words</title>', t + head, 1)
page = page.replace('<script>', offline_js + '<script>', 1)
open(os.path.join(HERE, 'index.html'), 'w').write(page)

sw = open(os.path.join(HERE, 'sw.js')).read()
sw = re.sub(r"const CACHE = 'italiano-\d+';", "const CACHE = 'italiano-%s';" % version, sw)
open(os.path.join(HERE, 'sw.js'), 'w').write(sw)

docs = {}
for path in ['progress/current', 'progress/sort', 'flash/stats', 'flash/focus', 'flash/later',
             'flash/examples', 'time/stats', 'practice/stats', 'check/stats']:
    f = os.path.join(seed_dir, path + '.json')
    if os.path.exists(f):
        docs[path] = json.load(open(f))
seed = {'generated': datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + 'Z', 'docs': docs}
json.dump(seed, open(os.path.join(HERE, 'data.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print('built', version, len(docs), 'docs')
