# main.py
#
# Copyright 2026 - 2030 Sreetx
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Import modul dasar

import os, sys, time, threading, glob, subprocess, shutil, builtins, tempfile, struct
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

tmp_file = tempfile.gettempdir()
if not os.path.exists(os.path.join(tmp_file, "sxcc", "extracted_frames", "png")):
    os.makedirs(os.path.join(tmp_file, "sxcc", "extracted_frames", "png"), exist_ok=True)
if not os.path.exists(os.path.join(tmp_file, "sxcc", "extracted_frames", "cur")):
    os.makedirs(os.path.join(tmp_file, "sxcc", "extracted_frames", "cur"), exist_ok=True)

png_dir = os.path.join(tmp_file, "sxcc", "extracted_frames", "png")
name_dir = os.path.join(tmp_file, "sxcc", "sxcc_history_name")
cur_dir = os.path.join(tmp_file, "sxcc", "extracted_frames", "cur")
name_file = os.path.join(tmp_file, "sxcc", "sxcc.link")

with open (name_file, 'r', encoding='UTF-8') as f:
    name_file = f.read().strip().lower()
    name_file = name_file.split(os.sep)[-1].split('.')[0]

hotspot_x = 0
hotspot_y = 0
size = 32
half = size // 2

CURSOR_MAPPING = {
    "normal": ["left_ptr", "default", "arrow", "top_left_arrow", "alias", "b66166c04f8c3109214a4fbd64a50fc8", "center_ptr", "context-menu", "d9ce0ab605698f320427677b458ad60b", "right_ptr", "size-bdiag", "size-fdiag", "size-ndia", "size-nesw", "size-nwse", "size-all", "up-arrow"],
    "link": ["hand2", "pointing_hand", "6430b46141f100e14c45121c210874e4", "b66166444125010022004241001a4768", "copy", "dnd-copy", "dnd-link", "dnd-move", "dnd-none", "e29285e634086352946a0e7090d73106", "hand1", "link", "pointer"],
    "busy": ["wait", "watch", "0426c178a3d1912440f09a0000000000", "spinning"],
    "working": ["left_ptr_watch", "progress", "3ecb6120745662f87724a141450a241d", "half-busy", "left_ptr_watch", "left_ptr_progress"],
    "text": ["xterm", "text", "ibeam", "vbeam"],
    "unavailable": ["circle", "crossed", "not-allowed", "03b6e0fcb3499374a867c041f52298f", "crossed_circle", "dnd-no-drop", "forbidden", "prohibited", "no-drop"],
    "help": ["question_arrow", "help", "whats_this", "d9ce0ab4e3f143c393bc1440003208b3", "left_ptr_help", "help_center"],
    "move": ["move", "fleur", "all-scroll", "d4c3b1e7a9f100e14c45121c210874e4", "close_hand", "open_hand", "grab", "grabbing"],
    "horizontal": ["h_double_arrow", "size_hor", "sb_h_double_arrow", "col-resize", "left_side", "right_side", "e-resize", "ew-resize", "w-resize"],
    "vertical": ["h_double_arrow", "size_hor", "sb_h_double_arrow", "col-resize", "left_side", "right_side", "bottom_side", "n-resize", "ns-resize", "top_side", "row-resize", "s-resize"],
    "pin": ["location", "pin", "map", "d9ce0ab4e3f143c393bc1440003208b3", "color-picker"],
    "precision": ["crosshair", "cross", "tcross", "cross_reverse", "cell", "plus", "precision", "zoom-in", "zoom-out"],
    "handwriting": ["pencil", "draft", "fossil"],
    "alternate": ["up_arrow", "center_ptr"],
    "diagonal1": ["nwse-resize", "size_bdiag", "top_left_corner", "bottom_right_corner", "bd_double_arrow", "nw-resize", "size_fdiag", "se-resize"],
    "diagonal2": ["nesw-resize", "size_fdiag", "top_right_corner", "bottom_left_corner", "fd_double_arrow", "ne-resize", "size_bdiag", "sw-resize"],
}

HOTSPOT_SPECIAL = {
    "precision" : (5, 6),
    "text" : (4, 8),
    "busy" : (half, half),
    "move" : (half, half),
    "horizontal" : (half, half),
    "vertical" : (half, half),
    "diagonal1" : (half, half),
    "diagonal2" : (half, half),
}
# Penamaan tema kursor
with open(name_dir, 'r', encoding='UTF-8') as f:
    name_cursors = f.read().strip()
    if name_cursors == "":
        name_cursors = "My_Cursor_Theme"

# Index theme
INDEX_THEME = f"""[Icon Theme]
Name={name_cursors}
Comment=Custom Cursor Theme created by SXCC (Sreetx Cross Cursors Converter)!
"""

def compiler_xcur():
    #Output path
    if not os.path.exists(os.path.expanduser(os.path.join("~", "Downloads", f"{name_cursors}", "cursors"))):
        os.makedirs(os.path.expanduser(os.path.join("~", "Downloads", f"{name_cursors}", "cursors")), exist_ok=True)
    output_path = os.path.expanduser(os.path.join("~", "Downloads", f"{name_cursors}", "cursors"))

    output_path_up = os.path.expanduser(os.path.join("~", "Downloads", f"{name_cursors}"))

    key_type = name_file.lower()

    # Tulis konfig kursor
    conf_path = os.path.join(png_dir, "cursor.conf")
    png_files = sorted([p for p in os.listdir(png_dir) if p.endswith('.png')])

    x_hot, y_hot = HOTSPOT_SPECIAL.get(key_type, (0, 0))

    with open(conf_path, 'w') as f:
        for p in png_files:
            f.write(f"{size} {x_hot} {y_hot} {os.path.join(png_dir, p)} 70\n")

    # Panggil xcursorgen untuk buat XCursor
    try:
        master = os.path.join(png_dir, "master")
        subprocess.run(['xcursorgen', str(conf_path), master], check=True)
        aliases = CURSOR_MAPPING.get(key_type.lower(), [key_type])
        for alias in aliases:
            dest_path = os.path.join(output_path, alias)
            shutil.copy2(master, dest_path)

    except subprocess.CalledProcessError as e:
        rprint(f"[white on red] FAIL [/] Error during XCursor generation: {e}")
    
    with open(os.path.join(output_path_up, "index.theme"), 'w') as f:
        f.write(INDEX_THEME)

    if os.path.exists(png_dir):
        shutil.rmtree(png_dir)
    if os.path.exists(cur_dir):
        shutil.rmtree(cur_dir)

    rprint(f"[bold cyan]![/] XCursor created with [yellow]Xcursorgen[/]: {output_path}")
    rprint(f"[bold cyan]![/] Successfully created cursor file: {', '.join(aliases)}")