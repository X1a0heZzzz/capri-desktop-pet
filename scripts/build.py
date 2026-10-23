"""Rebuild approved atlases from preserved transparent pose sources."""
from pathlib import Path
import argparse
import shutil
import numpy as np
from PIL import Image
from common import ROOT, catalogue, read_json
from validate import validate

def normalize_groups(folders):
    groups = []
    for folder in folders:
        base = ROOT / 'sources/frames' / folder
        items = []
        for rec in read_json(base / 'frames.json')['frames']:
            image = Image.open(base / rec['file']).convert('RGBA')
            box = rec['crop_box']
            ratio = 512 / (box[2] - box[0])
            ox = (rec['sheet_origin'][0] - box[0]) * ratio
            oy = (rec['sheet_origin'][1] - box[1]) * ratio
            items.append((image, ratio, ox, oy))
        groups.append(items)
    flat = [item for group in groups for item in group]
    left = min(i[2] for i in flat)
    top = min(i[3] for i in flat)
    right = max(i[2] + i[0].width*i[1] for i in flat)
    bottom = max(i[3] + i[0].height*i[1] for i in flat)
    scale = min(180 / (right-left), 192 / (bottom-top))
    normalized = []
    for group in groups:
        result = []
        for cell, ratio, ox, oy in group:
            rgba = np.array(cell)
            alpha = rgba[:, :, 3]
            alpha[alpha < 8] = 0
            alpha[alpha > 245] = 255
            rgba[alpha == 0, :3] = 0
            cell = Image.fromarray(rgba)
            size = (round(cell.width*ratio*scale), round(cell.height*ratio*scale))
            cell = cell.convert('RGBa').resize(size, Image.Resampling.LANCZOS).convert('RGBA')
            x = round((192-(right-left)*scale)/2 + (ox-left)*scale)
            y = round(208-12-(bottom-top)*scale + (oy-top)*scale)
            frame = Image.new('RGBA', (192, 208))
            frame.alpha_composite(cell, (x, y))
            result.append(frame)
        normalized.append(result)
    return normalized

def shifted(image, x=0, y=0):
    frame = Image.new('RGBA', image.size)
    frame.alpha_composite(image, (x, y))
    return frame

def assemble(rest, expr, clear):
    rows = [
        [expr[0], rest[0], rest[1], rest[2], rest[5], expr[7] if clear else rest[1]],
        [shifted(expr[1], x, y) for x,y in [(-3,0),(-2,-1),(-1,-2),(0,-3),(1,-2),(2,-1),(3,0),(0,0)]],
        [shifted(expr[2], x, y) for x,y in [(3,0),(2,-1),(1,-2),(0,-3),(-1,-2),(-2,-1),(-3,0),(0,0)]],
        [expr[6], expr[3], rest[3], expr[8]],
        [expr[0], shifted(expr[4],0,-2), shifted(expr[4],0,-5), shifted(expr[4],0,-2), expr[0]],
        [expr[0], expr[7], rest[0], rest[1], rest[2], rest[5], rest[2], rest[1]],
        [rest[2], shifted(rest[2],0,-1), rest[4], rest[5], expr[5], rest[2]],
        [expr[0], expr[6], expr[1], expr[0], expr[2], expr[6]],
        [expr[6], expr[3], expr[8], rest[3], expr[8], expr[0]],
    ]
    sheet = Image.new('RGBA', (1536,1872))
    for row, frames in enumerate(rows):
        for col, frame in enumerate(frames):
            sheet.alpha_composite(frame, (col*192,row*208))
    return sheet

def build(output):
    for entry in catalogue()['pets']:
        pet_id = entry['id']
        folder = output / 'pets' / pet_id
        folder.mkdir(parents=True, exist_ok=True)
        if pet_id == 'capri-pixel':
            sheet = Image.open(ROOT / 'sources/pixel/atlas-1x.png').convert('RGBA')
            sheet = sheet.resize((1536,1872), Image.Resampling.NEAREST)
        else:
            clear = pet_id == 'capri-clear'
            names = ['chibi-rest-extracted','chibi-expressions-extracted'] if clear else ['rest-v2-extracted','expressions-v2-extracted']
            sheet = assemble(*normalize_groups(names), clear=clear)
        sheet.save(folder / 'spritesheet.png')
        sheet.save(folder / 'spritesheet.webp', lossless=True, exact=True)
        for name in ['pet.json','animation-manifest.json']:
            shutil.copy2(ROOT / entry['package'] / name, folder / name)
    return validate(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/rebuilt')
    args = parser.parse_args()
    import json
    print(json.dumps(build(args.output.resolve()), ensure_ascii=False, indent=2))
