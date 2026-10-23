"""Check approved package pixels, frame geometry and distributable paths."""
import argparse
from pathlib import Path
from PIL import Image, ImageChops
from common import ROOT, SHEET, STATES, catalogue, read_json, pixel_hash

def validate(root=ROOT, check_fingerprint=True):
    root = Path(root)
    preview_data = ROOT / 'docs/preview-data.js'
    if preview_data.exists():
        import json
        text = preview_data.read_text(encoding='utf-8')
        assert text.startswith('window.CAPRI = ') and text.endswith(';\n')
        assert json.loads(text[len('window.CAPRI = '):-2]) == catalogue(), 'Preview data is stale; run scripts/update_preview.py'
    results = []
    for entry in catalogue()['pets']:
        folder = root / entry['package']
        meta = read_json(folder / 'pet.json')
        manifest = read_json(folder / 'animation-manifest.json')
        assert meta['id'] == entry['id'], f'{folder}: ID mismatch'
        assert meta['spriteVersionNumber'] == 1, f'{folder}: expected legacy v1'
        assert meta['spritesheetPath'] == 'spritesheet.webp', f'{folder}: unsafe sprite path'
        png = Image.open(folder / 'spritesheet.png').convert('RGBA')
        webp = Image.open(folder / 'spritesheet.webp').convert('RGBA')
        assert png.size == webp.size == SHEET, f'{folder}: incorrect dimensions'
        assert png.tobytes() == webp.tobytes(), f'{folder}: PNG/WebP pixels differ'
        assert png.getchannel('A').getextrema() == (0, 255), f'{folder}: transparency missing'
        assert len(manifest['states']) == 9
        for row, state in enumerate(manifest['states']):
            count = state['frames']
            assert state['row'] == row and state['state'] == STATES[row]
            assert type(count) is int and 1 <= count <= 8
            assert len(state['durationsMs']) == count
            assert all(type(v) is int and v > 0 for v in state['durationsMs'])
            for col in range(count):
                frame = png.crop((col*192, row*208, (col+1)*192, (row+1)*208))
                assert frame.getchannel('A').getbbox(), f'{folder}: empty {row}/{col}'
            if count < 8:
                blank = png.crop((count*192, row*208, 1536, (row+1)*208))
                assert blank.getchannel('A').getbbox() is None, f'{folder}: nonblank unused cells'
        digest = pixel_hash(png)
        if check_fingerprint:
            assert digest == entry['rgbaSha256'], f'{folder}: approved pixels changed'
        results.append({'id': entry['id'], 'frames': sum(s['frames'] for s in manifest['states']),
                        'rgbaSha256': digest, 'status': 'pass'})
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    import json
    print(json.dumps(validate(args.root), ensure_ascii=False, indent=2))
