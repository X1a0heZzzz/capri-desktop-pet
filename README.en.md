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
cells. They contain key poses and small rigid translations, not motion-interpolated
video or a newly generated sixteen-direction v2 set. Host playback timings can differ.

## Build

Python 3.12 and `pip install -r requirements.txt`, then:

```sh
python scripts/build.py
python scripts/validate.py
python scripts/release.py
```

Builds go to `dist/rebuilt/`; packaged releases and SHA-256 checksums go to `dist/`.
No image generation, paid API, installer, host binary or local account state is required.
See [build notes](docs/BUILD.md) for pixel-source preservation and reproduction limits.

Code and documentation: [MIT](LICENSE). Character images and identity are **excluded**
from MIT; see [ASSET_RIGHTS.md](ASSET_RIGHTS.md). Unofficial, AI-assisted fan art;
no claim of character ownership, endorsement or commercial clearance.
