"""Clear edition v1.1: edge cleanup and host-speed choreography.

Every frame is derived from the preserved transparent pose sources. Poses are
never redrawn; the only additions are whole-pose transforms (bob, lean,
squash/stretch), independent drift of the detached hair shards, mirrored
running-left frames, and closed-eye blinks painted over the original eyes.
Work happens at 3x cell resolution and is downsampled once at the end.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from common import ROOT, read_json

SS = 3
CELL_W, CELL_H = 192, 208
BASELINE = CELL_H - 12
OUTLINE = (22, 4, 18)

# Codex / Petdex default host timings for a v1 atlas (see docs/BUILD.md).
HOST_DURATIONS = {
    'idle': [280, 110, 110, 140, 140, 320],
    'running-right': [120] * 7 + [220],
    'running-left': [120] * 7 + [220],
    'waving': [140, 140, 140, 280],
    'jumping': [140, 140, 140, 140, 280],
    'failed': [140] * 7 + [240],
    'waiting': [150] * 5 + [260],
    'running': [120] * 5 + [220],
    'review': [150] * 5 + [280],
}


def clean_edges(image, recolor_rim):
    """Drop the soft background smudge, sharpen the alpha ramp and unify the outline colour."""
    rgba = np.array(image.convert('RGBA')).astype(np.float32)
    alpha = rgba[..., 3]
    core = alpha >= 200
    near_core = ndimage.binary_dilation(core, iterations=2)
    alpha[~near_core] = 0
    alpha[:] = np.clip((alpha - 40) * 255 / (230 - 40), 0, 255)
    if recolor_rim:
        # The rest-pose sheet was matted from a violet backdrop and kept a violet rim.
        r, g, b = rgba[..., 0], rgba[..., 1], rgba[..., 2]
        edge = ndimage.distance_transform_edt(alpha > 0) <= 9
        violet = (r >= 25) & (b > r + 12) & (g < 60) & (b > 55)
        mask = edge & violet & (alpha > 0)
        for channel, value in enumerate(OUTLINE):
            rgba[..., channel][mask] = value
    # Semi-transparent fringe keeps whatever it sat on; pull it towards the outline colour.
    fringe = (alpha > 0) & (alpha < 255)
    dark = rgba[..., :3].max(axis=2) < 110
    for channel, value in enumerate(OUTLINE):
        rgba[..., channel][fringe & dark] = value
    rgba[alpha == 0, :3] = 0
    return Image.fromarray(rgba.round().astype(np.uint8))


def eye_blobs(image):
    """Return (cx, cy, r) for the two blue irises, largest first, left to right."""
    rgba = np.array(image).astype(int)
    r, g, b, a = (rgba[..., i] for i in range(4))
    blue = (b > 150) & (r < 90) & (g < 170) & (a > 200)
    labels, count = ndimage.label(blue)
    sizes = ndimage.sum(blue, labels, range(1, count + 1))
    keep = [i + 1 for i in np.argsort(-sizes)[:2] if sizes[i] > 60]
    blobs = []
    for label in keep:
        ys, xs = np.nonzero(labels == label)
        blobs.append((xs.mean(), ys.mean(), max(np.ptp(xs), np.ptp(ys)) / 2 + 1))
    return sorted(blobs)


def blink(image):
    """Paint closed eyes over the open ones, inside the green visor only."""
    rgba = np.array(image).copy()
    r, g, b, a = (rgba[..., i].astype(int) for i in range(4))
    green = (g > 170) & (r < 120) & (b < 150) & (a > 200)
    blobs = eye_blobs(image)
    assert len(blobs) == 2, 'expected two eyes'
    visor_green = np.median(rgba[green][:, :3], axis=0).astype(np.uint8)
    height, width = green.shape
    yy, xx = np.mgrid[0:height, 0:width]
    eye_ink = ((b > 120) & (r < 120)) | ((r > 200) & (g > 200) & (b > 200)) | ((g > 80) & (b > 80) & (r < 60))
    for cx, cy, radius in blobs:
        outer = radius * 1.95
        disc = (xx - cx) ** 2 + (yy - cy) ** 2 <= outer ** 2
        # Visor interior: between the outermost green pixels of each row near the eye.
        inside = np.zeros_like(disc)
        for y in range(int(cy - outer) - 1, int(cy + outer) + 2):
            if 0 <= y < height:
                row = np.nonzero(green[y, max(0, int(cx - outer * 2.2)):int(cx + outer * 2.2)])[0]
                if row.size:
                    start = max(0, int(cx - outer * 2.2))
                    inside[y, start + row.min():start + row.max() + 1] = True
        # Hair can cover the visor edge, so also take any iris, highlight or teal ring ink.
        fill = disc & (inside | eye_ink) & (a > 0)
        rgba[fill, :3] = visor_green
    canvas = Image.fromarray(rgba)
    scale = 4
    overlay = Image.new('RGBA', (width * scale, height * scale))
    draw = ImageDraw.Draw(overlay)
    for cx, cy, radius in blobs:
        # A relaxed closed eye: the lower arc of a flat ellipse, sitting on the old eye line.
        box = ((cx - radius * 1.2) * scale, (cy - radius * 0.95) * scale,
               (cx + radius * 1.2) * scale, (cy + radius * 0.4) * scale)
        draw.arc(box, 20, 160, fill=OUTLINE + (255,), width=max(2, round(radius * 0.5 * scale)))
    overlay = overlay.resize((width, height), Image.Resampling.LANCZOS)
    canvas.alpha_composite(overlay)
    return canvas


class Pose:
    """One source pose placed in a supersampled cell, split into body and loose shards."""

    def __init__(self, image, ratio, ox, oy, frame):
        left, top, right, bottom, scale = frame
        k = ratio * scale * SS
        size = (round(image.width * k), round(image.height * k))
        cell = image.convert('RGBa').resize(size, Image.Resampling.LANCZOS)
        x = round(((CELL_W - (right - left) * scale) / 2 + (ox - left) * scale) * SS)
        y = round((BASELINE - (bottom - top) * scale + (oy - top) * scale) * SS)
        canvas = Image.new('RGBa', (CELL_W * SS, CELL_H * SS))
        canvas.paste(cell, (x, y))
        full = np.array(canvas).astype(np.float32)
        alpha = full[..., 3] > 24
        labels, count = ndimage.label(ndimage.binary_dilation(alpha, iterations=2))
        sizes = ndimage.sum(alpha, labels, range(1, count + 1))
        body = labels == int(np.argmax(sizes)) + 1
        self.body = full * body[..., None]
        self.shards = full * (~body)[..., None]
        ys, xs = np.nonzero(body & alpha)
        self.pivot = (float(xs.mean()), float(ys.max()))

    def render(self, dx=0, dy=0, rot=0, sx=1.0, sy=1.0, shard=(0, 0), mirror=False):
        # Premultiplied "over": shards drift independently and may pass in front of the body.
        moved = ndimage.shift(self.shards, (shard[1] * SS, shard[0] * SS, 0), order=1)
        layer = moved + self.body * (1 - moved[..., 3:] / 255)
        layer = Image.fromarray(np.clip(layer, 0, 255).round().astype(np.uint8), 'RGBa')
        px, py = self.pivot
        if (sx, sy, rot) != (1.0, 1.0, 0):
            # Scale and lean about the base so the pose stays planted on its baseline.
            theta = np.radians(rot)
            c, s = np.cos(theta), np.sin(theta)
            m = np.array([[c * sx, -s * sy], [s * sx, c * sy]])
            inv = np.linalg.inv(m)
            offset = np.array([px, py]) - inv @ np.array([px, py])
            layer = layer.transform(layer.size, Image.Transform.AFFINE,
                                    (inv[0, 0], inv[0, 1], offset[0], inv[1, 0], inv[1, 1], offset[1]),
                                    resample=Image.Resampling.BICUBIC)
        out = Image.new('RGBa', layer.size)
        out.paste(layer, (round(dx * SS), round(dy * SS)))
        if mirror:
            out = out.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        return out


def downsample(layer):
    small = layer.resize((CELL_W, CELL_H), Image.Resampling.LANCZOS).convert('RGBA')
    rgba = np.array(small)
    rgba[rgba[..., 3] < 4] = 0
    return Image.fromarray(rgba)


def load_poses(folders, rim_groups):
    groups = []
    for folder in folders:
        base = ROOT / 'sources/frames' / folder
        items = []
        for rec in read_json(base / 'frames.json')['frames']:
            image = clean_edges(Image.open(base / rec['file']), folder in rim_groups)
            box = rec['crop_box']
            ratio = 512 / (box[2] - box[0])
            ox = (rec['sheet_origin'][0] - box[0]) * ratio
            oy = (rec['sheet_origin'][1] - box[1]) * ratio
            items.append((image, ratio, ox, oy))
        groups.append(items)
    flat = [item for group in groups for item in group]
    left = min(i[2] for i in flat)
    top = min(i[3] for i in flat)
    right = max(i[2] + i[0].width * i[1] for i in flat)
    bottom = max(i[3] + i[0].height * i[1] for i in flat)
    frame = (left, top, right, bottom, min(180 / (right - left), 192 / (bottom - top)))
    return groups, frame


def clear_rows():
    (rest, expr), frame = load_poses(['chibi-rest-extracted', 'chibi-expressions-extracted'],
                                     {'chibi-rest-extracted'})
    pose = lambda item, closed=False: Pose(blink(item[0]) if closed else item[0], *item[1:], frame)
    # Expression board order follows sources/prompts/chibi-expressions-prompt.txt.
    stand, stand_blink = pose(expr[0]), pose(expr[0], True)
    drift = pose(expr[1])
    effort, effort_blink = pose(expr[2]), pose(expr[2], True)
    excited, wave, shock = pose(expr[4]), pose(expr[6]), pose(expr[7])
    droop, kneel, chin, chin_blink = pose(rest[0]), pose(rest[1]), pose(rest[2]), pose(rest[2], True)
    tease, lounge = pose(rest[3]), pose(rest[4])

    # Calm floating breath with one blink; slow-timed hosts land on neutral frames.
    idle = [stand.render(), stand.render(dy=-1, sy=1.01, shard=(0, -1)), stand_blink.render(dy=-1, sy=1.01, shard=(0, -1)),
            stand.render(dy=-2, sy=1.02, shard=(0, -2)), stand.render(dy=-1, sy=1.01, shard=(0, -1)), stand.render(shard=(0, 1))]

    # The right-looking drift pose, two floating hops per cycle, leaning into travel; shards trail behind.
    # Left is the same frames mirrored in place, so the gaze turns with the direction.
    hop = []
    for i in range(8):
        lift = abs(np.sin(np.pi * i / 4))
        contact = 1 - lift
        hop.append(dict(dy=-7 * lift, rot=4 + 2 * np.sin(np.pi * i / 4), sx=1 + 0.03 * contact, sy=1 - 0.035 * contact + 0.02 * lift,
                        shard=(-3, 2 * lift - 1)))
    right = [drift.render(**h) for h in hop]
    left = [drift.render(**h, mirror=True) for h in hop]

    waving = [stand.render(), wave.render(rot=4, shard=(-1, -1)), wave.render(rot=-3, shard=(1, 0)), wave.render(rot=4, shard=(-1, -1))]

    jumping = [stand.render(sx=1.05, sy=0.92, shard=(0, 1)), excited.render(dy=-12, sx=0.97, sy=1.04, shard=(0, 3)),
               excited.render(dy=-22, shard=(0, 1)), excited.render(dy=-11, sy=1.02, shard=(0, -3)),
               stand.render(sx=1.03, sy=0.96)]

    # Startle, droop, kneel, flop: a short readable collapse.
    failed = [shock.render(), droop.render(dy=1), droop.render(dy=2, sy=0.98, shard=(0, 1)), kneel.render(),
              kneel.render(sy=0.985, shard=(0, 1)), lounge.render(), lounge.render(sy=1.012, shard=(0, -1)), lounge.render(shard=(0, 1))]

    waiting = [chin.render(), chin.render(sy=1.008, shard=(0, -1)), chin.render(sy=1.015, shard=(0, -2)),
               chin.render(sy=1.008, shard=(0, -1)), chin_blink.render(), chin.render(shard=(0, 1))]

    # Busy, slightly flustered bobbing with a quick blink; no foot-running.
    running = [effort.render(), effort.render(dy=-2, rot=1.5, shard=(1, -1)), effort.render(dy=0, shard=(0, 1)),
               effort.render(dy=-2, rot=-1.5, shard=(-1, -1)), effort_blink.render(), effort.render(dy=-1, shard=(0, 0))]

    review = [tease.render(), tease.render(rot=-2, shard=(0, -1)), tease.render(dy=1, rot=-3.5, shard=(1, -1)),
              tease.render(rot=-2, shard=(0, 0)), tease.render(), tease.render(dy=-1, rot=1, shard=(0, 1))]

    return [[downsample(f) for f in row] for row in
            [idle, right, left, waving, jumping, failed, waiting, running, review]]
