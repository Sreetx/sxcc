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

root_png = os.path.join(tmp_dir, "sxcc", "extracted_frames", "png")
root_cur = os.path.join(tmp_dir, "sxcc", "extracted_frames", "cur")

def convert_cur_to_png():
    for folder_name in os.listdir(root_cur):
        cur_dir = os.path.join(root_cur, folder_name)
        png_dir = os.path.join(root_png, folder_name)

        if not os.path.isdir(cur_dir): continue

        # Buat Folder Mirror
        os.makedirs(png_dir, exist_ok=True)
        rprint(f'\n[black on cyan] * [/] Converting Folder: {folder_name}\n'); time.sleep(2)
        cur_files = sorted([f for f in os.listdir(cur_dir) if f.endswith('.cur')])

        for index, filename in enumerate(cur_files):
            cur_path = os.path.join(cur_dir, filename)
            png_path = os.path.join(png_dir, f"frame_{index+1:03d}.png")

            try:
                with Image.open(cur_path) as img:
                    rgba_img = img.convert("RGBA")
                    datas = rgba_img.getdata()
                    new_data = [(0, 0, 0, 0) if (item[0] < 2 and item[1] < 2 and item[2] < 2) else item for item in datas]
                    rgba_img.putdata(new_data)
                    rgba_img.save(png_path, "PNG")

                    rprint(f' [black on green]*[/] Converting {filename} [dim]→[/] frame_{index+1:03d}.png'); time.sleep(0.1)
            except Exception as e:
                rprint(f"[black on red] FAIL [/] {filename}: {e}")

    rprint(f'\n[black on green] * [/] All frames saved in {root_png}')