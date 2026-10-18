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

import os, sys, time, threading, glob, subprocess, shutil, builtins, tempfile, vtracer, re
from pathlib import Path
from PIL import Image
import os
from rich import print as rprint

tmp_dir = tempfile.gettempdir()

root_png = os.path.join(tmp_dir, "sxcc", "extracted_frames", "png")
os.makedirs(root_png, exist_ok=True)

root_cur = os.path.join(tmp_dir, "sxcc", "extracted_frames", "cur")
os.makedirs(root_cur, exist_ok=True)

root_upscale = os.path.join(tmp_dir, "sxcc", "extracted_frames", "upscale")
os.makedirs(root_upscale, exist_ok=True)
                            
root_svg = os.path.join(tmp_dir, "sxcc", "extracted_frames", "svg")
os.makedirs(root_svg, exist_ok=True)

SCALE = 8
PAD = 2

def convert_ani_to_png():
    for folder_name in os.listdir(root_cur):
        cur_dir = os.path.join(root_cur, folder_name)
        png_dir = os.path.join(root_png, folder_name)

        if not os.path.isdir(cur_dir): continue

        os.makedirs(png_dir, exist_ok=True)

        rprint(f'\n[black on cyan] * [/] Converting: {folder_name}\n'); time.sleep(1.5)
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

                    rprint(f' [black on green]*[/] Converting {filename} [dim]→[/] frame_{index+1:03d}.png'); time.sleep(0.07)
            except Exception as e:
                rprint(f"[black on red] FAIL [/] {filename}: {e}")

    rprint(f'\n[black on green] ✔ [/] All frames saved in {root_png}')

def upscale_the_pngs(scale=SCALE, pad=PAD, pixel_art=True):
    rprint ("\n[black on cyan] ~ [/] Upscaling frames...")
    method = Image.NEAREST if pixel_art else Image.LANCZOS

    for folder_name in os.listdir(root_png):
        png_dir = os.path.join(root_png, folder_name)
        upscale_dir = os.path.join(root_upscale, folder_name)

        if not os.path.isdir(png_dir): continue
        os.makedirs(upscale_dir, exist_ok=True)

        png_files = sorted([f for f in os.listdir(png_dir) if f.endswith(".png")])

        for index, filename in enumerate(png_files):
            png_path = os.path.join(png_dir, filename)
            upscaled_path = os.path.join(upscale_dir, f"frame_{index+1:03d}.png")

            try:
                with Image.open(os.path.join(png_path)) as img:
                    img = img.convert("RGBA")
                    canvas = Image.new("RGBA", (img.width + pad*2, img.height + pad*2), (0, 0, 0, 0))
                    canvas.paste(img, (pad, pad))
                    canvas = canvas.resize((canvas.width * scale, canvas.height * scale), method)
                    canvas.save(os.path.join(upscaled_path), "PNG")
            except Exception as e:
                rprint(f"[bold red] ! [/]Error: {e}")

    rprint(" [black on green]*[/] Done!"); time.sleep(1)

def fix_svg_size(svg_path, scale=SCALE, pad=PAD):
    text = Path(svg_path).read_text()

    m = re.search(r'<svg\b[^>]*>', text)
    if not m: return
    tag = m.group(0)

    w_m = re.search(r'\bwidth="(\d+)', tag)
    h_m = re.search(r'\bheight="(\d+)', tag)
    if not (w_m and h_m): return

    w = int(w_m.group(1)) // scale - pad * 2
    h = int(h_m.group(1)) // scale - pad * 2

    new_tag = re.sub(r'\s(width|height|viewBox)="[^"]*"', '', tag)
    new_tag = new_tag[:-1] + (
        f' width="{w}" height="{h}"'
        f' viewBox="{pad*scale} {pad*scale} {w*scale} {h*scale}">'
    )
    Path(svg_path).write_text(text.replace(tag, new_tag, 1))

def convert_png_to_svg():
    rprint ("\n[black on cyan] > [/] Converting frames to SVG...")
    for folder_name in os.listdir(root_png):
        upscale_dir = os.path.join(root_upscale, folder_name)
        svg_dir = os.path.join(root_svg, folder_name)

        if not os.path.isdir(upscale_dir): continue
        os.makedirs(svg_dir, exist_ok=True)

        upscale_png_files = sorted([f for f in os.listdir(upscale_dir) if f.endswith('.png')])
        for index, filename in enumerate(upscale_png_files):
            png_path = os.path.join(upscale_dir, filename)
            svg_path = os.path.join(svg_dir, f"frame_{index+1:03d}.svg")

            try:
                vtracer.convert_image_to_svg_py(png_path, svg_path)
                fix_svg_size(svg_path)
            except Exception as e:
                rprint (f"[bold red] ! [/]{e}")

    rprint (" [black on cyan]✔[/] Done!"); time.sleep(1)



