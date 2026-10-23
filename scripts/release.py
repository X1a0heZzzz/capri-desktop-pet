"""Validate and create deterministic release ZIPs with SHA-256 checksums."""
import argparse
from pathlib import Path
import hashlib
import zipfile
from common import ROOT, catalogue
from validate import validate

EXCLUDED = {'.git','.venv','__pycache__','dist','work','.pytest_cache'}

def zip_files(target, pairs):
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, name in sorted(pairs, key=lambda item: item[1]):
            info = zipfile.ZipInfo(name, date_time=(2026,10,23,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())

def release(output):
    validate()
    output.mkdir(parents=True, exist_ok=True)
    version = catalogue()['version']
    products = []
    for entry in catalogue()['pets']:
        slug = entry['id']
        folder = ROOT / entry['package']
        pairs = [(p, slug + '/' + p.name) for p in folder.iterdir() if p.is_file()]
        pairs.append((ROOT / 'ASSET_RIGHTS.md', slug + '/ASSET_RIGHTS.md'))
        target = output / f'{slug}-v{version}.zip'
        zip_files(target, pairs)
        products.append(target)
    sources = [(p, 'capri-artwork/' + p.relative_to(ROOT / 'sources').as_posix())
               for p in (ROOT / 'sources').rglob('*') if p.is_file()]
    sources.append((ROOT / 'ASSET_RIGHTS.md', 'capri-artwork/ASSET_RIGHTS.md'))
    target = output / f'capri-artwork-v{version}.zip'
    zip_files(target, sources)
    products.append(target)
    files = [(p, 'capri-desktop-pet/' + p.relative_to(ROOT).as_posix()) for p in ROOT.rglob('*')
             if p.is_file() and not any(s in EXCLUDED for s in p.relative_to(ROOT).parts)
             and p.suffix not in {'.pyc','.zip'}]
    target = output / f'capri-desktop-pet-source-v{version}.zip'
    zip_files(target, files)
    products.append(target)
    checksums = '\n'.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name for p in products) + '\n'
    (output / 'SHA256SUMS.txt').write_text(checksums, encoding='utf-8')
    return [{'file': p.name, 'bytes': p.stat().st_size} for p in products]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    import json
    print(json.dumps(release(args.output.resolve()), indent=2))
