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
from PIL import Image
import os
from rich import print as rprint

tmp_dir = tempfile.gettempdir()
if not os.path.exists(os.path.join(tmp_dir, "sxcc", "extracted_frames", "png")):
    os.makedirs(os.path.join(tmp_dir, "sxcc", "extracted_frames", "png"), exist_ok=True)

png_dir = os.path.join(tmp_dir, "sxcc", "extracted_frames", "png")
cur_dir = os.path.join(tmp_dir, "sxcc", "extracted_frames", "cur")

def convert_cur_to_png():
    cur_files = sorted([f for f in os.listdir(cur_dir) if f.endswith('.cur')])
    total = len(cur_files)
    index = 0
    while index < total:
        filename = cur_files[index]
        cur_path = os.path.join(cur_dir, filename)
        png_name = f"frame_{index+1:03d}.png"
        png_path = os.path.join(png_dir, png_name)

        try:
            with Image.open(str(cur_path)) as img:
                img = img.convert("RGBA")
                datas = img.getdata()

                rgba_img = img.convert("RGBA")

                datas = rgba_img.getdata()
                new_data = []

                for item in datas:
                    if item[0] < 2 and item[1] < 2 and item[2] < 2:
                        new_data.append((0, 0, 0, 0))
                    else:
                        new_data.append(item)
                rgba_img.putdata(new_data)
                rgba_img.save(str(png_path), "PNG")
            
            # [/] buat reset tema universal
            rprint(f"[black on green]#[/] Converting frame {index+1:03d} [dim]→[/] [green]{png_name}[/]")
            time.sleep(0.1) 
            
        except Exception as e:
            rprint(f"[white on red] FAIL [/] {filename}: {e}")
            rprint(' [*] Skipping this frame and moving to the next one.')

        index += 1

    rprint(f"\n[bold green] * [/bold green][orange1]{total}[/orange1] frames converted to PNG in: {png_dir}")