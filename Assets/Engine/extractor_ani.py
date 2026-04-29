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
path_jembatan = os.path.join(temp_dir, "sxcc", "sxcc.link")
with open (path_jembatan, 'r', encoding='UTF-8') as f:
    ani = f.read().strip()

name_frame = ani.split(os.sep)[-1].split('.')[0]

def ekstrak():
    if not os.path.exists(os.path.join(temp_dir, "sxcc", "extracted_frames")):
        os.makedirs(os.path.join(temp_dir, "sxcc", "extracted_frames"), exist_ok=True)

    if not os.path.exists(os.path.join(temp_dir, "sxcc", "extracted_frames", "cur")):
        os.makedirs(os.path.join(temp_dir, "sxcc", "extracted_frames", "cur"), exist_ok=True)

    with open(ani, 'rb') as f:
        content = f.read()

    frame_count = 0
    pos = 0

    print ("")
    while True:
        pos = content.find(b'icon', pos)
        if pos == -1:
            break

        size_pos = pos + 4
        chunk_size = struct.unpack('<I', content[size_pos:size_pos+4])[0]
        
        start_data = size_pos + 4
        icon_data = content[start_data : start_data + chunk_size]
        
        if len(icon_data) > 40 and icon_data[0] == 0x28:
            # Ambil Width & Height asli dari DIB
            w = struct.unpack('<I', icon_data[4:8])[0]
            h = struct.unpack('<I', icon_data[8:12])[0]

            header = b'\x00\x00\x02\x00\x01\x00' # Reserved, Type 2, Count 1
            entry = struct.pack('<BBBBHHII', 
                w if w < 256 else 0, 
                (h // 2) if h < 512 else 0, 
                0, 0, 0, 0, len(icon_data), 22)
            final_data = header + entry + icon_data
        else:
            final_data = icon_data
        
        frame_count += 1
        output_path = os.path.join(temp_dir, "sxcc", "extracted_frames", "cur", f"{name_frame}_{frame_count:03d}.cur")
        
        with open(output_path, 'wb') as icon_file:
            icon_file.write(final_data)
        
        rprint(f"[black on green]*[/black on green] Extracting {name_frame}_{frame_count:03d}.cur to Cur")
        pos = start_data + chunk_size
        time.sleep (0.1)

    if frame_count == 0:
        rprint("\n [bold red]![/bold red] Frame not detected, check if it is an ani file or not!"); sys.exit()
    else:
        rprint(f"\n[bold green] * [/bold green][orange1]{frame_count}.cur[/orange1] frames extracted to: {os.path.join(temp_dir, 'sxcc', 'extracted_frames', 'cur')}")
