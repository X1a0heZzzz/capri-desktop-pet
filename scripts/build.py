"""Rebuild the three atlases from preserved transparent pose sources."""
from pathlib import Path
import argparse
import shutil
from PIL import Image
from common import ROOT, catalogue, pixel_hash, write_json
from choreography import anime_rows, clear_rows, pixel_rows
from validate import validate

def sheet_from_rows(rows):
    sheet = Image.new('RGBA', (1536,1872))
    for row, frames in enumerate(rows):
        for col, frame in enumerate(frames):
            sheet.alpha_composite(frame, (col*192,row*208))
    return sheet

def sheets():
    clear = clear_rows()
    return {'capri-anime': sheet_from_rows(anime_rows()),
            'capri-pixel': sheet_from_rows(pixel_rows(clear)),
            'capri-clear': sheet_from_rows(clear)}

def build(output):
    for pet_id, sheet in sheets().items():
        entry = next(p for p in catalogue()['pets'] if p['id'] == pet_id)
        folder = output / 'pets' / pet_id
        folder.mkdir(parents=True, exist_ok=True)
        sheet.save(folder / 'spritesheet.png')
        sheet.save(folder / 'spritesheet.webp', lossless=True, exact=True)
        for name in ['pet.json','animation-manifest.json']:
            shutil.copy2(ROOT / entry['package'] / name, folder / name)
    return validate(output)

def approve():
    """Write rebuilt atlases into pets/ and record their fingerprints (after an intended art change)."""
    data = catalogue()
    for pet_id, sheet in sheets().items():
        folder = ROOT / 'pets' / pet_id
        sheet.save(folder / 'spritesheet.png', optimize=True)
        sheet.save(folder / 'spritesheet.webp', lossless=True, exact=True, method=6)
        next(p for p in data['pets'] if p['id'] == pet_id)['rgbaSha256'] = pixel_hash(sheet)
    write_json(ROOT / 'catalogue.json', data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/rebuilt')
    parser.add_argument('--approve', action='store_true', help='replace the packaged atlases and fingerprints')
    args = parser.parse_args()
    if args.approve:
        approve()
        print('Updated pets/*/spritesheet.* and catalogue.json; run scripts/update_preview.py next')
    else:
        import json
        print(json.dumps(build(args.output.resolve()), ensure_ascii=False, indent=2))
