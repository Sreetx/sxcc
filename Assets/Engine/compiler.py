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

import os, sys, time, shutil, tempfile, json
from pathlib import Path
from rich import print as rprint

# Modul Clickgen dari AUR dan PyPi versi waras. Jangan kau install yang legacy!
from clickgen.parser import open_blob
from clickgen.writer import to_x11

# Set the tmp dir
tmp_file = tempfile.gettempdir()
root_temp = os.path.join(tmp_file, "sxcc")
frames_cache_dir = os.path.join(root_temp, "extracted_frames")

png_dir = os.path.join(frames_cache_dir, "png")
name_dir = os.path.join(root_temp, "sxcc_history_name")
cur_dir = os.path.join(frames_cache_dir, "cur")
name_file = os.path.join(root_temp, "sxcc.link")
svg_dir = os.path.join(frames_cache_dir, "svg")

# Penamaan tema kursor
with open(name_dir, 'r', encoding='UTF-8') as f:
    name_cursors = f.read().strip()
    if name_cursors == "":
        name_cursors = "My_Cursor_Theme"

with open (name_file, 'r', encoding='UTF-8') as f:
    name_file = f.read().strip().lower()
    name_file = name_file.split(os.sep)[-1].split('.')[0]

# Destinasi kursor
final_output = os.path.expanduser(os.path.join("~", "Downloads", f"{name_cursors}"))
os.makedirs(final_output, exist_ok=True)

output_path = os.path.expanduser(os.path.join(final_output, "cursors"))
os.makedirs(output_path, exist_ok=True)

cursor_scalable_output = os.path.expanduser(os.path.join(final_output, "cursors_scalable"))
os.makedirs(cursor_scalable_output, exist_ok=True)

# Metadata cursors, kita fix dulu ke 32 size kursor nya. Nanti di patch depan baru di tambahin
hotspot_x = 0
hotspot_y = 0
size = 32
half = size // 2
setengah = half // 2
delay = 100

CURSOR_MAPPING = {
    "normal": ["left_ptr", "default", "arrow", "top_left_arrow", "alias", "b66166c04f8c3109214a4fbd64a50fc8", "context-menu", "d9ce0ab605698f320427677b458ad60b", "size-bdiag", "size-fdiag", "size-ndia", "size-nesw", "size-nwse", "size-all"],
    "link": ["hand2", "pointing_hand", "6430b46141f100e14c45121c210874e4", "b66166444125010022004241001a4768", "copy", "dnd-copy", "dnd-link", "dnd-move", "dnd-none", "e29285e634086352946a0e7090d73106", "hand1", "link", "pointer"],
    "busy": ["wait", "watch", "0426c178a3d1912440f09a0000000000", "spinning"],
    "working": ["left_ptr_watch", "progress", "3ecb6120745662f87724a141450a241d", "half-busy", "left_ptr_progress"],
    "text": ["xterm", "text", "ibeam", "vbeam"],
    "unavailable": ["circle", "crossed", "not-allowed", "03b6e0fcb3499374a867c041f52298f", "crossed_circle", "dnd-no-drop", "forbidden", "prohibited", "no-drop"],
    "help": ["question_arrow", "help", "whats_this", "d9ce0ab4e3f143c393bc1440003208b3", "left_ptr_help", "help_center"],
    "move": ["move", "fleur", "all-scroll", "d4c3b1e7a9f100e14c45121c210874e4", "close_hand", "open_hand", "grab", "grabbing"],
    "horizontal": ["h_double_arrow", "size_hor", "sb_h_double_arrow", "col-resize", "e-resize", "ew-resize", "w-resize", "left_side", "right_side"],
    "vertical": ["v_double_arrow", "size_ver", "sb_v_double_arrow", "row-resize", "n-resize", "ns-resize", "s-resize", "top_side", "bottom_side"],
    "pin": ["location", "pin", "map", "d9ce0ab4e3f143c393bc1440003208b3", "color-picker"],
    "precision": ["crosshair", "cross", "tcross", "cross_reverse", "cell", "plus", "precision", "zoom-in", "zoom-out"],
    "handwriting": ["pencil", "draft", "fossil"],
    "alternate": ["up_arrow", "center_ptr", "right_ptr"],
    "diagonal1": ["size_bdiag", "nwse-resize", "top_left_corner", "bottom_right_corner", "bd_double_arrow", "nw-resize", "se-resize"],
    "diagonal2": ["size_fdiag", "nesw-resize", "top_right_corner", "bottom_left_corner", "fd_double_arrow", "ne-resize", "sw-resize"],
}

HOTSPOT_SPECIAL = {
    "precision" : (5, 6),
    "text" : (4, 8),
    "link" : (5, 1),
    "unavailable" : (setengah, setengah),
    "alternate" : (5, 2),
    "busy" : (half, half),
    "move" : (half, half),
    "horizontal" : (half, half),
    "vertical" : (half, half),
    "diagonal1" : (half, half),
    "diagonal2" : (half, half),
    "person" : (4, 4),
    "pin": (4, 11),
}

# Index theme
INDEX_THEME = f"""[Icon Theme]
Name={name_cursors}
Comment=Custom Cursor Theme created by SXCC (Sreetx Cross Cursors Converter)!
"""

def compiler_xcur():
    print("")
    # Creating Index.theme
    with open(os.path.join(final_output, "index.theme"), 'w') as f:
        f.write(INDEX_THEME)

    # Start shorting the cursor frames

    for folder_name in os.listdir(png_dir):
        current_png_dir = os.path.join(png_dir, folder_name)
        if not os.path.isdir(current_png_dir): continue
        rprint (f' [black on cyan]*[/] Building {folder_name} (Clickgen)'); time.sleep(1)
        
        png_files = sorted([os.path.join(current_png_dir, p) for p in os.listdir(current_png_dir) if p.endswith('.png')])
        if not png_files: continue

        png_data = []
        for p in png_files:
            with open(p, 'rb') as f:
                png_data.append(f.read())

        x_hot, y_hot = HOTSPOT_SPECIAL.get(folder_name.lower(), (1, 1))

        try:
            cur = open_blob(png_data, hotspot=(x_hot, y_hot), delay=delay)
            xcursor_binary = to_x11(cur.frames)
            aliases = CURSOR_MAPPING.get(folder_name.lower(), [folder_name.lower()])
            for alias in aliases:
                dest = os.path.join(output_path, alias)
                with open (dest, 'wb') as f:
                    f.write(xcursor_binary)

        except Exception as e:
            rprint(f"\n[white on red] FAIL [/] Error during XCursor generation for {folder_name}: {e}")

# Creating SVG in this moment
def svg_cursor_creator ():
    # FInal path of SVG Cursors

    rprint (f"\n[blue] </> [/]Creating Index.theme\n")

    # Buat Index.theme dulu
    with open(os.path.join(final_output, "index.theme"), 'w') as f:
        f.write(INDEX_THEME)

    if not os.path.exists(svg_dir):
        rprint (f"[red] ! [/]Extracted frames not found on {svg_dir}"); sys.exit()

    # Terus kita deteksi apakah frame ada atau tidak di tmp, walau fungsi ini udah ada di awal kode, apa salahnya kan masang lagi biar gk keteteran
    for folder_name in os.listdir(svg_dir):
        src_folder = os.path.join(svg_dir, folder_name)
        if not os.path.exists(src_folder):
            continue

        category_name = folder_name.lower()
        category_folder = os.path.join(cursor_scalable_output, category_name)
        os.makedirs(category_folder, exist_ok=True)

        category_print = category_folder.split()[-1]

        # Kita mulai copy frames secara mentah dari /tmp/sxcc/extracted_frames/png/xxx ke folder tujuan di ~/Downloads
        copied_frames = []
        for file_names in sorted(os.listdir(src_folder)):
            if file_names.lower().endswith(".svg"):
                src_file = os.path.join(src_folder, file_names)
                dst_name = os.path.join(category_folder, file_names)
                file_names_print = file_names.split()[-1]
                shutil.copy(src_file, dst_name)
                copied_frames.append(file_names)

                rprint (f" [black on cyan]>[/] Copying {file_names_print} → {category_name}"); time.sleep(0.05)

        # Untuk kordinat kursor
        hx, xy = HOTSPOT_SPECIAL.get(category_name, (hotspot_x, hotspot_y))

        # Koentji nya ada di sini biar kursor nya gerak
        rprint ("\n[black on cyan] ~ [/] Creating metadata")
        metadata_list = []
        for file_names in copied_frames:
            item = {
                "filename" : file_names,
                "delay" : int(delay),
                "hotspot_x" : int(hx),
                "hotspot_y" : int(xy),
                "nominal_size" : int(size)
            }
            metadata_list.append(item)

        meta_path = os.path.join(category_folder, "metadata.json")
        with open(meta_path, "w", encoding="utf-8") as meta_file:
            json.dump(metadata_list, meta_file, indent=4)

        rprint (" [black on cyan]✔[/] Done!\n"); time.sleep(0.7)

        # Kita buat symlink di kode ini biar kursor nya kompatibel
        for category, aliases in CURSOR_MAPPING.items():
            if not aliases:
                continue

            unique_aliases = list(dict.fromkeys(aliases))
            for alias in unique_aliases:
                if alias.lower() == category.lower():
                    continue

                symlink_path = os.path.join(cursor_scalable_output, alias)

                if os.path.lexists(symlink_path):
                    if os.path.isdir(symlink_path) and not os.path.isdir(symlink_path):
                        shutil.rmtree(symlink_path)

                    else:
                        #tambahin gini biar tools gk mati konyol
                        try:
                            os.remove(symlink_path)
                        except OSError:
                            pass

                # Buat symlink
                try:
                    os.symlink(category, symlink_path)
                except Exception as e:
                    rprint(f"[bold red] ! [/] Error: {e}")

    # Bersihkan file temporary setelah selesai
    if os.path.exists(png_dir):
        shutil.rmtree(png_dir)
    if os.path.exists(cur_dir):
        shutil.rmtree(cur_dir)
    
    # Ending
    rprint(f"[black on green]✔[/] XCursors saved on [bold white]{output_path}")
    rprint(f"[black on green]✔[/] SVG Cursors saved on [bold white]{cursor_scalable_output}[/]")
    rprint(f"[black on green]✔[/] Cursors saved on [bold white]{final_output}[/]")
    rprint(f"[black on green]✔[/] You can copy [bold white]'{Path(final_output).name}'[/] to [bold orange1]/usr/share/icons/[/]")
                
