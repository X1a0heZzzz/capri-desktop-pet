"""Regenerate local preview data from the canonical catalogue."""
import json
from common import ROOT, catalogue

if __name__ == '__main__':
    serialized = json.dumps(catalogue(), ensure_ascii=False, separators=(',',':'))
    (ROOT / 'docs/preview-data.js').write_text('window.CAPRI = ' + serialized + ';\n', encoding='utf-8')
    print('Updated docs/preview-data.js')
