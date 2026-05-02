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

import os, sys, time, threading, glob, subprocess, shutil, builtins, tempfile
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich import print as rprint
import os
import struct

# Rich Console
console = Console()

# Path ke tempf global
temp_dir = tempfile.gettempdir()

# Path ani dari jembatan
def ekstrak():
    #Cek dan buat direktori jika belum ada
    if not os.path.exists(os.path.join(temp_dir, "sxcc", "extracted_frames")):
        os.makedirs(os.path.join(temp_dir, "sxcc", "extracted_frames"), exist_ok=True)
    if not os.path.exists(os.path.join(temp_dir, "sxcc", "extracted_frames", "cur")):
        os.makedirs(os.path.join(temp_dir, "sxcc", "extracted_frames", "cur"), exist_ok=True)

    # Baca path dari jembatan
    sxcc_link = os.path.join(temp_dir, "sxcc", "sxcc.link").strip()

    with open(sxcc_link, 'r', encoding='UTF-8') as f:
        list_ani = [line.strip() for line in f if line.strip()]

    for ani_path in list_ani:
        rprint(f"\n[black on cyan] * [/] Extracting: {os.path.basename(ani_path)}\n"); time.sleep(1)
        if not os.path.exists(ani_path):
            rprint(f"[red] ! [/]File .ani Not found in: {ani_path}"); time.sleep(0.3)
            continue
        pos = 0
        frame_count = 0

        # Baca konten file .ani
        name_frame = os.path.basename(ani_path).split('.')[0]
        base_extract_dir = os.path.join(temp_dir, "sxcc", "extracted_frames", "cur", name_frame)
        os.makedirs(base_extract_dir, exist_ok=True)

        with open(ani_path, 'rb') as f:
            content = f.read()

        while True:
            pos = content.find(b'icon', pos)
            if pos == -1: break

            size_pos = pos + 4
            chunk_size = struct.unpack('<I', content[size_pos:size_pos+4])[0]
            
            start_data = size_pos + 4
            icon_data = content[start_data : start_data + chunk_size]
        
            if len(icon_data) > 40 and icon_data[0] == 0x28:
                w = struct.unpack('<I', icon_data[4:8])[0]
                h = struct.unpack('<I', icon_data[8:12])[0]
                header = b'\x00\x00\x02\x00\x01\x00'
                entry = struct.pack('<BBBBHHII', w if w < 256 else 0, (h // 2) if h < 512 else 0, 0, 0, 0, 0, len(icon_data), 22)
                final_data = header + entry + icon_data
            else:
                final_data = icon_data
            
            frame_count += 1
            output_path = os.path.join(base_extract_dir, f"{name_frame}_{frame_count:03d}.cur")
            
            with open(output_path, 'wb') as cur_file:
                cur_file.write(final_data)
            
            rprint(f" [black on green]*[/] Extracting {name_frame}[dim] → [/]{name_frame}_{frame_count:03d}"); time.sleep(0.1)
            pos = start_data + chunk_size
        
    return frame_count 

