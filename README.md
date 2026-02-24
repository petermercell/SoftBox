# SoftBox

**Soft shadow area light for Nuke 17 ScanlineRender2**

By Marten Blumen

![Nuke 17](https://img.shields.io/badge/Nuke-17.0%2B-yellow) ![License](https://img.shields.io/badge/license-MIT-blue) ![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

ScanlineRender2's built-in lights only cast hard shadows. SoftBox produces smooth, physically plausible penumbras by emitting a grid of sub-lights spread across a rectangular light surface — the same technique used in production VFX before stochastic shadow sampling became standard.

## Features

- **Soft shadows** via multi-light grid (1 to 64+ sub-lights)
- **Artist-friendly** — single Shadow Samples knob controls quality vs speed
- **Energy conserving** — total illumination stays constant regardless of sample count
- **Full transform** — translate, rotate, scale via standard Axis_knob
- **Viewport wireframe** — orange rectangle with direction arrow
- **USD native** — creates standard DiskLightPrims on the scene graph

## Installation

### From Release

1. Download `AreaLight.dll` from [Releases](../../releases)
2. Copy `AreaLight.dll` and `menu.py` to `~/.nuke/`
3. Restart Nuke 17
4. Find **AreaLight** under **3D > Lights** in the toolbar

### Build From Source

Requires **Visual Studio 2022** and **CMake 3.20+**.

```bash
git clone https://github.com/YOUR_USERNAME/SoftBox.git
cd SoftBox
cmake -S . -B build --preset vs2022
cmake --build build --config Release
```

The plugin is built to `build/plugin/AreaLight.dll`. To install:

```bash
cmake --install build
```

This copies `AreaLight.dll` and `menu.py` to `~/.nuke/`.

If Nuke is installed in a non-standard location:

```bash
cmake -S . -B build --preset vs2022 -DNUKE_DIR="D:/Apps/Nuke17.0v1"
```

## Usage

1. Create an **AreaLight** node and connect it to your scene
2. Set **Width** and **Height** for the light surface size
3. Adjust **Intensity**, **Exposure**, and **Color**
4. Set **Shadow Samples** to control shadow softness:

| Shadow Samples | Grid | Quality | Use Case |
|---|---|---|---|
| 1 | — | Hard shadow | Look-dev, fast iteration |
| 4 | 2×2 | Basic penumbra | Previz |
| 16 | 4×4 | Smooth | Recommended default |
| 64 | 8×8 | Very smooth | Final renders, close-ups |

5. Connect to **ScanlineRender2** and render

## How It Works

ScanlineRender2's DiskLight shader shoots a single shadow ray to the light centre, producing a hard edge. SoftBox creates N DiskLightPrims arranged in a grid across the rectangular surface. Each sub-light gets `intensity / N` so total illumination is conserved. The overlapping hard shadows from different positions blend into a smooth penumbra gradient.

Shadow softness is determined by the light's physical size (Width × Height). Shadow Samples controls the smoothness of the gradient, not the penumbra width.

## Tips

- Shadow softness = light size. Bigger light = wider penumbra
- Shadow Samples = smoothness. More samples = less banding
- Keep at 1 during look-dev, crank up for finals
- Render time scales linearly with sample count

## Project Structure

```
SoftBox/
├── UsdAreaLightOp.cpp    # Plugin implementation
├── UsdAreaLightOp.h      # Plugin header
├── CMakeLists.txt        # Build configuration
├── CMakePresets.json     # VS2022 preset
├── menu.py               # Nuke menu installer
├── LICENSE               # MIT license
└── README.md             # This file
```

## Requirements

- Nuke 17.0 or later
- Windows x64
- ScanlineRender2

## License

MIT — see [LICENSE](LICENSE) for details.
