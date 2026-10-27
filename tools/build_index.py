#!/usr/bin/env python3
"""Rebuild the LLM text layer for sources/public-records.

Usage (from repo root): python3 tools/build_index.py
Needs: pdftotext (poppler), beautifulsoup4, lxml. Optional: pdftoppm + tesseract (OCR of scanned PDFs).
Writes: sources/text/<id>.md, sources/INDEX.md, sources/MANIFEST.tsv. Never modifies originals.
Existing text files are kept (matched by sha256 prefix in front matter), so hand fixes survive.
Descriptions live in sources/descriptions.json (id -> kind, tier, date, desc).
"""
import os, re, sys, json, hashlib, subprocess, glob, collections, shutil, tempfile
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'sources/public-records')
OUT = os.path.join(ROOT, 'sources/text'); os.makedirs(OUT, exist_ok=True)
DESC = json.load(open(os.path.join(ROOT, 'sources/descriptions.json'), encoding='utf8'))
TERMS = {'CAIR': r'\bCAIR\b', 'Awad': r'Awad', 'Nihad': r'Nihad', 'Ahmad/Yehya': r'Ahmad|Yehya|Yehia', 'Brotherhood': r'Brotherhood'}

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def slug(n):
    s = re.sub(r'\.(pdf|html)$', '', n, flags=re.I)
    return re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()[:60]

def clean(t):
    t = t.replace('­', '')
    t = re.sub(r'-\n(?=[a-z])', '', t)
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r' ?\n ?', '\n', t)
    return re.sub(r'\n{3,}', '\n\n', t).strip()

def strip_line_numbers(body):
    lines = body.split('\n')
    lone = [l for l in lines if re.fullmatch(r'\s*\d{1,2}\s*', l)]
    if len(lines) < 200 or len(lone) / len(lines) < 0.15: return body
    b = '\n'.join(l for l in lines if not re.fullmatch(r'\s*\d{1,2}\s*', l))
    return re.sub(r'\n{3,}', '\n\n', b)

def ocr(path):
    if not (shutil.which('pdftoppm') and shutil.which('tesseract')): return None
    tmp = tempfile.mkdtemp(); pre = os.path.join(tmp, 'p')
    subprocess.run(['pdftoppm', '-r', '200', '-gray', '-png', path, pre], check=True)
    parts = []
    for i, im in enumerate(sorted(glob.glob(pre + '-*.png'))):
        t = subprocess.run(['tesseract', im, '-', '--psm', '6'], capture_output=True).stdout.decode('utf8', 'replace')
        t = re.sub(r'\n{3,}', '\n\n', re.sub(r'[ \t]+', ' ', t)).strip()
        parts.append('[p.%d]\n%s' % (i + 1, t))
    shutil.rmtree(tmp)
    return '\n\n'.join(parts)

def convert(path, sid, h):
    if path.lower().endswith(('.webp', '.jpg', '.jpeg', '.png')):
        print('IMAGE NEEDS HAND TRANSCRIPTION (withhold addresses, DOB, ID numbers):', path)
        fm = 'id: %s\nfile: sources/public-records/%s\nsha256: %s\ntype: image\npages: None\ntokens_est: 0\n' % (sid, os.path.basename(path), h[:16])
        open(os.path.join(OUT, sid + '.md'), 'w', encoding='utf8').write('---\n' + fm + '---\n\nTODO: transcribe by viewing the image.\n')
        return
    if path.lower().endswith('.pdf'):
        raw = subprocess.run(['pdftotext', '-enc', 'UTF-8', path, '-'], capture_output=True).stdout.decode('utf8', 'replace')
        pages = raw.split('\f')
        if pages and not pages[-1].strip(): pages = pages[:-1]
        body = '\n\n'.join('[p.%d]\n%s' % (i + 1, clean(pg)) for i, pg in enumerate(pages))
        npg, typ, note = len(pages), 'pdf', ''
        if len(body) < 400 * max(npg, 1) * 0.5:
            o = ocr(path)
            if o: body, note = o, 'ocr: tesseract-eng (verify quotes against the PDF image)\n'
        else:
            body = strip_line_numbers(body)
    else:
        soup = BeautifulSoup(open(path, encoding='utf8', errors='replace').read(), 'lxml')
        for t in soup(['script', 'style', 'nav', 'footer', 'header', 'form', 'noscript', 'svg', 'iframe', 'aside']): t.decompose()
        node = soup.find('article') or soup.find('main') or soup.body or soup
        body = clean(node.get_text('\n')); npg, typ, note = None, 'html', ''
    fm = 'id: %s\nfile: sources/public-records/%s\nsha256: %s\ntype: %s\npages: %s\ntokens_est: %d\n%s' % (
        sid, os.path.relpath(path, ROOT).replace('sources/public-records/', ''), h[:16], typ, npg, len(body) // 4, note)
    open(os.path.join(OUT, sid + '.md'), 'w', encoding='utf8').write('---\n' + fm + '---\n\n' + body + '\n')

def main():
    files = sorted(f for f in os.listdir(SRC) if os.path.isfile(os.path.join(SRC, f)) and f.lower().endswith(('.pdf', '.html', '.webp', '.jpg', '.jpeg', '.png')))
    seen, dups, canon = {}, collections.defaultdict(list), collections.OrderedDict()
    # keep ids stable: reuse the id whose front matter already carries this sha
    known = {}
    for p in glob.glob(os.path.join(OUT, '*.md')):
        m = re.search(r'^sha256: (\w+)', open(p, encoding='utf8').read(800), re.M)
        if m: known[m.group(1)] = os.path.basename(p)[:-3]
    for f in files:
        p = os.path.join(SRC, f); h = sha(p)
        if h in seen: dups[seen[h]].append(f); continue
        sid = known.get(h[:16]) or slug(f)
        seen[h] = sid; canon[sid] = (f, h)
        if not os.path.exists(os.path.join(OUT, sid + '.md')): convert(p, sid, h); print('converted', sid)
    # dedupe identical text under different bytes
    texthash = {}
    tsv = ['id\ttext_file\tkind\ttier\tdate\tpages\ttokens\thits\toriginal_file\tduplicates\tdescription']
    md = ['---\ntitle: Source index\n---\n# Source index (sources/text)\n\nOne row per distinct source file. Load `sources/text/<id>.md` only after reading the row. `hits` = keyword counts inside the text (CAIR, Awad, Nihad, Ahmad/Yehya, Brotherhood) so you can skip files that cannot answer the question. Originals stay in `sources/public-records/` (PDF/HTML). Court transcripts have line numbers removed. Files marked OCR may misread names; check the PDF image before quoting.\n\nTier: primary = court record, filing, official release. advocacy/party = leads only, cite the documents they reproduce.\n',
          '| id | kind | tier | date | pp | ~tok | hits | what it is |', '|---|---|---|---|---|---|---|---|']
    for sid, (f, h) in canon.items():
        txt = open(os.path.join(OUT, sid + '.md'), encoding='utf8').read()
        pages = re.search(r'^pages: (\w+)', txt, re.M).group(1)
        hits = ['%s %d' % (k, len(re.findall(p, txt))) for k, p in TERMS.items() if re.search(p, txt)]
        d = DESC.get(sid, {'kind': '?', 'tier': '?', 'date': '?', 'desc': 'NO DESCRIPTION: read log.md, then add to sources/descriptions.json'})
        ocr_tag = ' (OCR)' if 'ocr:' in txt[:700] else ''
        dup = ('; same bytes as: ' + ', '.join(dups[sid])) if dups[sid] else ''
        th = hashlib.md5(re.sub(r'\W', '', txt.split('---\n', 2)[2]).encode()).hexdigest()
        if th in texthash: dup += '; text identical to ' + texthash[th]
        texthash.setdefault(th, sid)
        md.append('| %s | %s | %s | %s | %s | %d | %s | %s%s%s |' % (sid, d['kind'], d['tier'], d['date'], '-' if pages == 'None' else pages, len(txt) // 4, '; '.join(hits) or '-', d['desc'], ocr_tag, dup))
        tsv.append('\t'.join([sid, 'sources/text/%s.md' % sid, d['kind'], d['tier'], d['date'], '' if pages == 'None' else pages, str(len(txt) // 4), '; '.join(hits), f, '|'.join(dups[sid]), d['desc']]))
    md.append('\nFiles under `*_files/` folders in sources/public-records are browser-saved page assets. Never open them.\n\nsources/log.md is the authoritative reading log (what was read in full, what was skimmed). Open leads: records/open-leads.md.')
    open(os.path.join(ROOT, 'sources/INDEX.md'), 'w', encoding='utf8').write('\n'.join(md) + '\n')
    open(os.path.join(ROOT, 'sources/MANIFEST.tsv'), 'w', encoding='utf8').write('\n'.join(tsv) + '\n')
    print(len(canon), 'sources;', sum(1 for s in canon if s not in DESC), 'without description')

if __name__ == '__main__': main()
