"""Shared, local-only package helpers. MIT; character assets excluded."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
CELL = (192, 208)
SHEET = (1536, 1872)
STATES = ['idle', 'running-right', 'running-left', 'waving', 'jumping',
          'failed', 'waiting', 'running', 'review']

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def catalogue():
    return read_json(ROOT / 'catalogue.json')

def pixel_hash(image):
    return hashlib.sha256(image.convert('RGBA').tobytes()).hexdigest()

def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
