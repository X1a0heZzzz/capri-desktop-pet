"""Copy one pet to an explicit local destination, refusing overwrites."""
import argparse
from pathlib import Path
import shutil
from common import ROOT, catalogue
from validate import validate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pet', choices=[p['id'] for p in catalogue()['pets']], default='capri-clear')
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    validate()
    target = args.destination.resolve() / args.pet
    if target.exists():
        parser.error(f'Destination already exists; nothing was overwritten: {target}')
    shutil.copytree(ROOT / 'pets' / args.pet, target)
    shutil.copy2(ROOT / 'ASSET_RIGHTS.md', target / 'ASSET_RIGHTS.md')
    print(f'Copied to {target}. Select this directory in a compatible host.')
