"""Render README previews from a package's encoded atlas at its manifest timings."""
import argparse
from PIL import Image, ImageDraw
from common import ROOT, catalogue, read_json

BACKGROUND = (231, 232, 238, 255)
# Stage gallery cards that are snapshots of a package (row, column of the atlas).
GALLERY = {'capri-pixel': '05-pixel-petdex', 'capri-clear': '06-clear-codex'}
GALLERY_CELLS = [(0, 0), (0, 2), (1, 3), (4, 2), (5, 0), (6, 0), (5, 6), (8, 2)]

def frames_of(entry):
    folder = ROOT / entry['package']
    sheet = Image.open(folder / 'spritesheet.webp').convert('RGBA')
    manifest = read_json(folder / 'animation-manifest.json')
    for state in manifest['states']:
        row = state['row']
        cells = [sheet.crop((c*192, row*208, (c+1)*192, (row+1)*208)) for c in range(state['frames'])]
        yield state, cells

def flatten(cell):
    frame = Image.new('RGBA', cell.size, BACKGROUND)
    frame.alpha_composite(cell)
    return frame.convert('RGB')

def render(pet_id, loop_ms=1800):
    entry = next(p for p in catalogue()['pets'] if p['id'] == pet_id)
    images, durations = [], []
    contact = Image.new('RGBA', (1536 + 128, 208*9), BACKGROUND)
    draw = ImageDraw.Draw(contact)
    for state, cells in frames_of(entry):
        # Play every state for roughly the same wall time so short loops stay visible.
        cycle = sum(state['durationsMs'])
        for _ in range(max(1, round(loop_ms / cycle))):
            for cell, duration in zip(cells, state['durationsMs']):
                images.append(flatten(cell))
                durations.append(duration)
        draw.text((8, state['row']*208 + 10), state['state'], fill=(90, 90, 100))
        for col, cell in enumerate(cells):
            contact.alpha_composite(cell, (128 + col*192, state['row']*208))
    target = ROOT / 'docs/previews'
    images[0].save(target / f'{pet_id}.gif', save_all=True, append_images=images[1:],
                   duration=durations, loop=0, optimize=True, disposal=1)
    contact.convert('RGB').save(target / f'{pet_id}-states.png', optimize=True)
    written = [target / f'{pet_id}.gif', target / f'{pet_id}-states.png']
    if pet_id in GALLERY:
        sheet = Image.open(ROOT / entry['package'] / 'spritesheet.webp').convert('RGBA')
        card = Image.new('RGBA', (768, 416), BACKGROUND)
        for i, (row, col) in enumerate(GALLERY_CELLS):
            card.alpha_composite(sheet.crop((col*192, row*208, (col+1)*192, (row+1)*208)), ((i % 4)*192, (i // 4)*208))
        written.append(ROOT / 'docs/gallery' / f'{GALLERY[pet_id]}.jpg')
        card.convert('RGB').save(written[-1], quality=92)
    return [str(path) for path in written]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pet', help='one package id; default renders all three')
    args = parser.parse_args()
    for pet_id in [args.pet] if args.pet else [p['id'] for p in catalogue()['pets']]:
        print('\n'.join(render(pet_id)))
