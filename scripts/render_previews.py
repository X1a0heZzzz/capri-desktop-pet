"""Render README previews from a package's encoded atlas at its manifest timings."""
import argparse
from PIL import Image, ImageDraw
from common import ROOT, catalogue, read_json

BACKGROUND = (231, 232, 238, 255)

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
    return [str(target / f'{pet_id}.gif'), str(target / f'{pet_id}-states.png')]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pet', default=catalogue()['defaultPet'])
    args = parser.parse_args()
    print('\n'.join(render(args.pet)))
