# Capri Desktop Pet

[简体中文](README.md) · **[Download latest release](https://github.com/X1a0heZzzz/capri-desktop-pet/releases/latest)**

Six production stages of Capri / 摩羯, preserved as source artwork and three legacy
8×9 desktop-pet packages: refined anime, pixel chibi and clear chibi.

![Clear edition](docs/previews/capri-clear.gif)

## Start

Download and extract the repository. Open `index.html` locally for an offline,
interactive nine-state preview. Choose `pets/capri-clear/` for the recommended
package, `pets/capri-pixel/` for the pixel edition or `pets/capri-anime/` for the
refined anime edition. Read [installation](docs/INSTALL.md) for host-specific limits.

The six stages are initial study, rest pose study, refined anime, chibi source art,
pixel export and clear export. Stages 1, 2 and 4 are design sources, not six separate
working applications. The renamed clear edition uses the same approved image data.

All three sheets are transparent, 1536×1872 pixels, 8 columns × 9 rows with 192×208
cells, not a newly generated sixteen-direction v2 set.

**v1.1 clear edition.** The recommended package was re-choreographed for the default
host speed of Codex and Petdex (about one second per loop). Idle is now a calm float with
breathing and a blink instead of cycling through six unrelated poses; travel rows look and
lean towards the direction of movement; failed is a startle-droop-kneel-flop collapse;
waiting is a chin-in-hand daydream. The soft dark smudge and violet rim left by the original
background removal were cleaned. Every frame still comes from the drawn source poses; the
only additions are whole-pose bob, lean and squash/stretch, independent hair-shard drift,
in-place mirroring and closed-eye lines painted over the original eyes. The anime and pixel
packages keep their v1.0 key-pose choreography, which was designed for slow timings.

![All clear-edition states](docs/previews/capri-clear-states.png)

## Build

Python 3.12 and `pip install -r requirements.txt`, then:

```sh
python scripts/build.py
python scripts/validate.py
python scripts/render_previews.py
python scripts/release.py
```

Builds go to `dist/rebuilt/`; packaged releases and SHA-256 checksums go to `dist/`.
No image generation, paid API, installer, host binary or local account state is required.
See [build notes](docs/BUILD.md) for pixel-source preservation and reproduction limits.

Code and documentation: [MIT](LICENSE). Character images and identity are **excluded**
from MIT; see [ASSET_RIGHTS.md](ASSET_RIGHTS.md). Unofficial, AI-assisted fan art;
no claim of character ownership, endorsement or commercial clearance.
