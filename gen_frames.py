import os
import random
import sys
import time
from datetime import datetime

import numpy as np
import yaml
from PIL import Image, ImageChops, ImageDraw, ImageFont


def load_config():
    # Priority: Command line argument > config.yml in current dir > screengen/config.yml
    if len(sys.argv) > 1 and sys.argv[1].endswith((".yml", ".yaml")):
        config_path = sys.argv[1]
    else:
        config_path = "config.yml"
        if not os.path.exists(config_path):
            config_path = "screengen/config.yml"

    print(f"Loading config from: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


CONFIG = load_config()

# Configuration from YAML
WIDTH, HEIGHT = CONFIG.get("width", 1920), CONFIG.get("height", 1080)
BG_COLOR = tuple(CONFIG.get("bg_color", [0, 0, 0]))
TEXT_COLOR = tuple(CONFIG.get("text_color", [0, 255, 0]))
FONT_SIZE = CONFIG.get("font_size", 18)
LINE_SPACING = CONFIG.get("line_spacing", 2)
OUTPUT_ROOT = "screengen/output"

# Global state for animation
progress_val = 0.0
tui_state = {
    "files": [],
    "total_size": 0,
    "current_dir": "/var/lib/docker/overlay2/data",
}


def draw_tui_ncdu(draw, font):
    """Draws an ncdu-style disk usage interface."""
    x, y = WIDTH - 600, 50
    w, h = 550, 400

    # Border
    draw.rectangle([x, y, x + w, y + h], outline=TEXT_COLOR, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=TEXT_COLOR)  # Header
    draw.text(
        (x + 10, y + 5), f"ncdu 1.15.1 ~ Use cursor keys", font=font, fill=BG_COLOR
    )

    # Content
    path_str = f"--- {tui_state['current_dir']} ---"
    draw.text((x + 10, y + 40), path_str, font=font, fill=TEXT_COLOR)

    # Fake file list
    if not tui_state["files"] or random.random() < 0.1:
        extensions = [".so", ".bin", ".log", ".cache", ".db", ".tmp"]
        tui_state["files"] = [
            {
                "name": f"lib_{os.urandom(2).hex()}{random.choice(extensions)}",
                "size": random.randint(10, 500),
            }
            for _ in range(12)
        ]
        tui_state["files"].sort(key=lambda x: x["size"], reverse=True)

    for i, f in enumerate(tui_state["files"]):
        color = TEXT_COLOR
        if i == (int(time.time() * 2) % 12):  # Simulate selection moving
            draw.rectangle(
                [x + 5, y + 70 + i * 25, x + w - 5, y + 70 + (i + 1) * 25],
                fill=(40, 40, 40),
            )

        size_bar = "#" * (f["size"] // 50)
        line = f"{f['size']:>5} MiB  [ {size_bar:<10} ]  {f['name']}"
        draw.text((x + 10, y + 72 + i * 25), line, font=font, fill=color)


def draw_tui_copy(draw, font):
    """Draws a verbose file copy stream."""
    x, y = WIDTH - 700, 50
    w, h = 650, 450

    if not tui_state.get("copy_logs"):
        tui_state["copy_logs"] = []

    # Add new copy lines
    for _ in range(int(CONFIG.get("tui_speed", 1.0) * 3)):
        fname = f"/usr/share/doc/package-{random.randint(100, 999)}/info_{os.urandom(4).hex()}.html"
        tui_state["copy_logs"].append(f"cp: '{fname}' -> '/mnt/backup/latest/'")

    tui_state["copy_logs"] = tui_state["copy_logs"][-18:]  # Keep 18 lines

    # Draw background box
    draw.rectangle([x, y, x + w, y + h], fill=(0, 20, 0, 150), outline=TEXT_COLOR)
    for i, log in enumerate(tui_state["copy_logs"]):
        draw.text((x + 10, y + 10 + i * 22), log, font=font, fill=TEXT_COLOR)


def draw_progress_bar(draw, font):
    """Apply a horizontal shift glitch to the image."""
    arr = np.array(img)
    rows, cols, channels = arr.shape
    for _ in range(random.randint(1, 5)):
        y_start = random.randint(0, rows - 20)
        y_end = y_start + random.randint(2, 20)
        shift = random.randint(-intensity, intensity)
        arr[y_start:y_end] = np.roll(arr[y_start:y_end], shift, axis=1)
    return Image.fromarray(arr)


def draw_progress_bar(draw, font):
    global progress_val
    bar_width = 400
    bar_height = 30
    x, y = (WIDTH - bar_width) // 2, HEIGHT - 100

    label = CONFIG.get("progress_label", "PROCESSING")
    progress_str = f"{label}: {int(progress_val * 100)}%"
    draw.text((x, y - 25), progress_str, font=font, fill=TEXT_COLOR)

    # Outer box
    draw.rectangle([x, y, x + bar_width, y + bar_height], outline=TEXT_COLOR, width=2)
    # Inner fill
    fill_w = int(bar_width * progress_val)
    if fill_w > 8:  # Ensure x1 >= x0 (4 + 4)
        draw.rectangle(
            [x + 4, y + 4, x + fill_w - 4, y + bar_height - 4], fill=TEXT_COLOR
        )

    # Increment
    progress_val = min(1.0, progress_val + CONFIG.get("progress_speed", 0.005))


def apply_glitch(img, intensity):
    """Apply a horizontal shift glitch to the image."""
    arr = np.array(img)
    rows, cols, channels = arr.shape
    for _ in range(random.randint(1, 5)):
        y_start = random.randint(0, rows - 20)
        y_end = y_start + random.randint(2, 20)
        shift = random.randint(-intensity, intensity)
        arr[y_start:y_end] = np.roll(arr[y_start:y_end], shift, axis=1)
    return Image.fromarray(arr)


def generate_hex_dump():
    addr = f"0x{random.randint(0x1000, 0xFFFF):04X}"
    bytes_data = " ".join([f"{random.randint(0, 255):02X}" for _ in range(8)])
    return (
        f"{addr}  {bytes_data}  |{''.join([random.choice('.-_/') for _ in range(8)])}|"
    )


COMPONENTS = [
    "kernel",
    "systemd",
    "udevd",
    "mount",
    "dhcpcd",
    "sshd",
    "dbus",
    "avahi",
    "crond",
    "ntpd",
    "docker",
    "kworker",
    "auditd",
    "lvm2",
]
ACTIONS = [
    "Starting",
    "Started",
    "Reached target",
    "Mounted",
    "Initializing",
    "Loading",
    "Configuring",
    "Checking",
    "Attaching",
    "Verifying",
]
TARGETS = [
    "Multi-User System",
    "Network Manager",
    "Local File Systems",
    "Cryptography Setup",
    "Kernel Modules",
    "Socket Store",
    "User Slice",
    "Basic System",
    "Encrypted Volume /dev/mapper/vault",
]


def generate_hex_dump():
    addr = f"0x{random.randint(0x1000, 0xFFFF):04X}"
    bytes_data = " ".join([f"{random.randint(0, 255):02X}" for _ in range(8)])
    return (
        f"{addr}  {bytes_data}  |{''.join([random.choice('.-_/') for _ in range(8)])}|"
    )


def generate_line():
    ts = f"[{random.uniform(0, 500):10.6f}] "
    chance = random.random()

    if chance < CONFIG.get("prob_hex_dump", 0.15):
        return ts + generate_hex_dump(), False

    if chance < CONFIG.get("prob_danger", 0.08):
        tags = ["(!!) CRITICAL", "(EE) ERROR", "[FATAL]", "!!! ALERT !!!"]
        msg = random.choice(
            [
                "STACK SMASHING DETECTED - ATTEMPTED EXPLOIT",
                "CPU CORE OVERHEAT - CLOCK SKEW DETECTED",
                "KERNEL PANIC: VFS: UNABLE TO MOUNT ROOT FS",
                "UNAUTHORIZED ACCESS ON PORT 22 - IP 192.168.1.104",
                "ENCRYPTION KEY EXFILTRATION DETECTED",
                "BUFFER OVERFLOW IN libc.so.6",
            ]
        )
        return ts + f"\033[91m{random.choice(tags)}: {msg}\033[0m", True

    if chance < CONFIG.get("prob_warning", 0.12):
        msg = f"Warning: {random.choice(['Unrecognized hardware ID', 'I/O Timeout on sda2', 'Entropy pool low', 'Deprecation warning: /proc/sys/kernel/low_entropy_behavior'])}"
        return ts + f"\033[93m{msg}\033[0m", False

    comp = random.choice(COMPONENTS)
    act = random.choice(ACTIONS)
    targ = random.choice(TARGETS)
    line = f"{ts} {comp}[{random.randint(1, 9999)}]: {act} {targ}."
    if "Started" in line or "Reached" in line or "Mounted" in line:
        line = f"{ts} [  \033[92mOK\033[0m  ] {act} {targ}."
    return line, False


def parse_and_draw(draw, text, pos, font):
    x, y = pos
    parts = text.split("\033[")
    current_color = TEXT_COLOR

    draw.text((x, y), parts[0], font=font, fill=current_color)
    x += draw.textlength(parts[0], font=font)

    for part in parts[1:]:
        if part.startswith("91m"):
            current_color = (255, 30, 30)
            content = part[3:]
        elif part.startswith("92m"):
            current_color = (100, 255, 100)
            content = part[3:]
        elif part.startswith("93m"):
            current_color = (255, 255, 100)
            content = part[3:]
        elif part.startswith("0m"):
            current_color = TEXT_COLOR
            content = part[2:]
        else:
            content = part

        if "\033[0m" in content:
            subparts = content.split("\033[0m")
            draw.text((x, y), subparts[0], font=font, fill=current_color)
            x += draw.textlength(subparts[0], font=font)
            current_color = TEXT_COLOR
            draw.text((x, y), subparts[1], font=font, fill=current_color)
            x += draw.textlength(subparts[1], font=font)
        else:
            draw.text((x, y), content, font=font, fill=current_color)
            x += draw.textlength(content, font=font)


def render_sequence():
    label = CONFIG.get("label", "boot")
    num_frames = CONFIG.get("num_frames", 120)
    lines_per_frame = CONFIG.get("lines_per_frame", 5)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(OUTPUT_ROOT, f"{label}_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "C:\\Windows\\Fonts\\consola.ttf",
    ]
    font = None
    for p in font_paths:
        if os.path.exists(p):
            font = ImageFont.truetype(p, FONT_SIZE)
            break
    if not font:
        font = ImageFont.load_default()

    line_height = FONT_SIZE + LINE_SPACING
    max_lines = (HEIGHT - 40) // line_height
    history = []

    print(f"Generating sequence: {label} ({num_frames} frames) to {output_dir}")

    for f in range(num_frames):
        for _ in range(lines_per_frame):
            line, is_danger = generate_line()
            history.append(line)

        visible_lines = history[-max_lines:]
        img = Image.new("RGB", (WIDTH, HEIGHT), color=BG_COLOR)
        draw = ImageDraw.Draw(img)

        if CONFIG.get("show_scanlines", True):
            for y in range(0, HEIGHT, 4):
                draw.line([(0, y), (WIDTH, y)], fill=(10, 15, 10))

        for i, line in enumerate(visible_lines):
            parse_and_draw(draw, line, (20, 20 + i * line_height), font)

        # New Feature: TUI Overlays
        if CONFIG.get("show_tui_overlay", True):
            t_type = CONFIG.get("tui_type", "ncdu")
            if t_type == "ncdu":
                draw_tui_ncdu(draw, font)
            elif t_type == "copy":
                draw_tui_copy(draw, font)

        # New Feature: Progress Bar
        if CONFIG.get("show_progress_bar", True):
            draw_progress_bar(draw, font)

        last_few = visible_lines[-10:]
        if any("CRITICAL" in l or "FATAL" in l or "ALERT" in l for l in last_few):
            overlay = Image.new("RGB", (WIDTH, HEIGHT), (150, 0, 0))
            img = Image.blend(img, overlay, CONFIG.get("flash_intensity", 0.2))

            if CONFIG.get("show_danger_banner", True):
                draw_overlay = ImageDraw.Draw(img)
                warning_text = " !! SYSTEM COMPROMISED !! "
                tw = draw_overlay.textlength(warning_text, font=font)
                draw_overlay.rectangle(
                    [
                        WIDTH // 2 - tw // 2 - 10,
                        HEIGHT // 2 - 30,
                        WIDTH // 2 + tw // 2 + 10,
                        HEIGHT // 2 + 30,
                    ],
                    fill=(255, 0, 0),
                )
                draw_overlay.text(
                    (WIDTH // 2 - tw // 2, HEIGHT // 2 - 10),
                    warning_text,
                    font=font,
                    fill=(255, 255, 255),
                )

        # New Feature: Glitch Effect
        if CONFIG.get("show_glitch", True) and random.random() < CONFIG.get(
            "glitch_chance", 0.1
        ):
            img = apply_glitch(img, CONFIG.get("glitch_intensity", 20))

        img.save(f"{output_dir}/frame_{f:04d}.png")
        if f % 20 == 0:
            print(f"Frame {f} saved.")


if __name__ == "__main__":
    render_sequence()
    print("Done!")
