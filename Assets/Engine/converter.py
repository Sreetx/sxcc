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

import os, time, tempfile, vtracer, re
from pathlib import Path
from PIL import Image
import os
from rich import print as rprint
from collections import deque

# Cache Directory
tmp_dir = tempfile.gettempdir()
root_tmp = os.path.join(tmp_dir, "sxcc")
frames_cache_dir = os.path.join(root_tmp, "extracted_frames")
os.makedirs(frames_cache_dir, exist_ok=True)

root_png = os.path.join(frames_cache_dir, "png")
os.makedirs(root_png, exist_ok=True)

root_cur = os.path.join(frames_cache_dir, "cur")
os.makedirs(root_cur, exist_ok=True)
                            
root_svg = os.path.join(frames_cache_dir, "svg")
os.makedirs(root_svg, exist_ok=True)

depth_style = os.path.exists(os.path.join(root_tmp, "depth_style"))
if depth_style:
    basic_or_upscale = os.path.join(frames_cache_dir, "png")
else:
    basic_or_upscale = os.path.join(frames_cache_dir, "upscale")

SCALE = 8
PAD = 2

# Cores utama untuk hapus background gambar
def remove_edge_background(img, threshold=2):
    """Hapus background hitam yang tersambung ke tepi gambar saja."""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()

    def is_bg(x, y):
        r, g, b, a = px[x, y]
        return a == 0 or (r < threshold and g < threshold and b < threshold)

    visited = [[False] * h for _ in range(w)]
    queue = deque()

    # Titik awal: semua pixel di keempat sisi gambar
    for x in range(w):
        for y in (0, h - 1):
            if is_bg(x, y) and not visited[x][y]:
                visited[x][y] = True
                queue.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg(x, y) and not visited[x][y]:
                visited[x][y] = True
                queue.append((x, y))

    # Flood fill (4 arah) -> hanya menyebar lewat pixel background
    while queue:
        x, y = queue.popleft()
        px[x, y] = (0, 0, 0, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny] and is_bg(nx, ny):
                visited[nx][ny] = True
                queue.append((nx, ny))

    return img

def convert_ani_to_png():
    for folder_name in os.listdir(root_cur):
        cur_dir = os.path.join(root_cur, folder_name)
        png_dir = os.path.join(root_png, folder_name)

        if not os.path.isdir(cur_dir): continue

        os.makedirs(png_dir, exist_ok=True)

        Image.init()

        # Buat ngecek file gambar yang bener. kalo nggak ya udah
        EKSTENSI = tuple(Image.registered_extensions().keys())

        # Kita eksekusi disini, dibawah kita pake EKSTENSI sebagai patokan untuk nyari file gambar yang punya akhiran .cur, .png, atau sebagainya.
        rprint(f'\n[black on cyan] * [/] Converting: {folder_name}\n'); time.sleep(0.7)
        cur_files = sorted([f for f in os.listdir(cur_dir) if f.endswith(EKSTENSI)])

        for index, filename in enumerate(cur_files):
            cur_path = os.path.join(cur_dir, filename)
            png_path = os.path.join(png_dir, f"frame_{index+1:03d}.png")

            try:
                with Image.open(cur_path) as img:
                    rgba_img = remove_edge_background(img, threshold=2)
                    rgba_img.save(png_path, "PNG")

                    rprint(f' [black on green]*[/] Converting {filename} [dim]→[/] frame_{index+1:03d}.png'); time.sleep(0.05)
            except Exception as e:
                rprint(f"[black on red] FAIL [/] {filename}: {e}")

    rprint(f'\n[black on green] ✔ [/] All frames saved in [bold white]{root_png}[/]')

def upscale_the_pngs(scale=SCALE, pad=PAD, pixel_art=True):
    rprint ("\n[black on cyan] ~ [/] Upscaling frames...")
    method = Image.NEAREST if pixel_art else Image.LANCZOS

    for folder_name in os.listdir(root_png):
        png_dir = os.path.join(root_png, folder_name)
        upscale_dir = os.path.join(basic_or_upscale, folder_name)

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

    rprint(" [black on green]*[/] Done!"); time.sleep(0.7)

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
        upscale_dir = os.path.join(basic_or_upscale, folder_name)
        svg_dir = os.path.join(root_svg, folder_name)

        if not os.path.isdir(upscale_dir): continue
        os.makedirs(svg_dir, exist_ok=True)

        upscale_png_files = sorted([f for f in os.listdir(upscale_dir) if f.endswith('.png')])
        for index, filename in enumerate(upscale_png_files):
            png_path = os.path.join(upscale_dir, filename)
            svg_path = os.path.join(svg_dir, f"frame_{index+1:03d}.svg")

            try:
                vtracer.convert_image_to_svg_py(png_path, svg_path)
                if depth_style:
                    pass
                else:
                    fix_svg_size(svg_path)
            except Exception as e:
                rprint (f"[bold red] ! [/]{e}")

    rprint (" [black on cyan]✔[/] Done!"); time.sleep(0.7)



