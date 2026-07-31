# TerminalGen 📟

A programmatic "Hollywood Hacker" terminal sequence generator. Perfect for 3D animation, VFX, and motion graphics projects.

Forget searching for expensive stock videos. Generate custom, high-resolution (4K ready), perfectly timed Linux-style boot sequences, file operations, and system panic screens.

## 🚀 Features

- **Realistic Linux Logs**: Randomized hardware checks, systemd service starts, and kernel logs.
- **TUIs (Text User Interfaces)**:
    - `ncdu` style disk usage scanner.
    - `cp -v` style verbose file copy streams.
- **Visual Effects**:
    - **Glitch**: Random horizontal displacement and data corruption.
    - **Danger Mode**: Flashing red overlays and "SYSTEM COMPROMISED" banners.
    - **Scanlines**: Subtle horizontal grid for that analog CRT feel.
- **Customizable**: Control everything via YAML "Recipes".
- **Image Sequences**: Outputs clean PNG frames—no compression artifacts, easy to import into Blender, C4D, or Unreal Engine.

## 🛠 Installation

```bash
# Clone the repo
git clone git@github.com:HristoVelev/terminalgen.git
cd terminalgen

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📖 Usage

### Run with default config:
```bash
python gen_frames.py
```

### Run with a specific Recipe:
```bash
python gen_frames.py recipes/panic_mode.yml
```

## 🍱 Recipes

Recipes are stored in `recipes/`. You can create your own by copying `recipes/template.yml`.

- `slow_boot.yml`: Realistic, calm system initialization.
- `panic_mode.yml`: High-speed scrolling, red text, heavy glitches, and meltdown alerts.
- `data_exfil.yml`: Verbose file copying TUI with a progress bar.

## ⚙️ Configuration

Edit `config.yml` or any recipe file to tweak:
- `lines_per_frame`: Scrolling speed.
- `text_color`: RGB values (e.g., Classic Green `[0, 255, 0]` or Amber `[255, 176, 0]`).
- `glitch_chance` & `glitch_intensity`: Control the chaos.
- `show_tui_overlay`: Toggle `ncdu` or `copy` modes.

## 📝 License
MIT
