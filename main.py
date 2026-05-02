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
import os, sys, time, threading, glob, subprocess, shutil, builtins, tempfile
from pathlib import Path
stop_event = threading.Event()
rprint = builtins.print

#Temp Super
tmp_dir = tempfile.gettempdir()
if not os.path.exists(os.path.join(tmp_dir, "sxcc")):
    os.makedirs(os.path.join(tmp_dir, "sxcc"), exist_ok=True)

# Cek Dependensi
try:
    def import_module():
        try:
            global banner
            from Assets.warna import banner
        except ImportError:
            print(" (*) File Assets/warna.py is Missing")
            print(" (*) Please reinstall this script from my github repository!"); sys.exit()
        
        # Cek Paket
        try:
            global Console
            global prompt
            global HTML
            global ANSI
            global Table
            global Panel
            global Text
            global rprint
            global FileHistory
            global AutoSuggestFromHistory
            from prompt_toolkit.formatted_text import HTML 
            from prompt_toolkit import prompt
            from rich.table import Table
            from rich.panel import Panel
            from rich.text import Text
            from urllib.parse import urlparse
            from prompt_toolkit.history import FileHistory
            from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

            try:
                import rich
                rprint = rich.print
            except ImportError:
                rprint = builtins.print
            import requests
            from PIL import Image
            from io import BytesIO
            from term_image.image import AutoImage
            from rich.console import Console

            global banner
            from Assets.warna import banner

        except ImportError:
            stop_event.set()
            rprint("\n * Required packages are missing!")
            chos = input(" ? Do you want to install the required packages now? (Y/n): ").strip()
            if chos.upper() == "Y":
                if sys.platform in ["linux", "linux2"]:
                    cmd_add = '--break-system-packages'
                else:
                    cmd_add = ""
                rprint(" * Installing packages...")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "rich", "prompt_toolkit", "term-image", "pillow", cmd_add])
                except subprocess.CalledProcessError:
                    pass

                if sys.platform in ['linux', 'linux2']:
                    rprint(f' * Checking modules installed with package manager!')
                    def get_package_manager():
                    # Daftar manager yang didukung, urutan menentukan prioritas
                        managers = {
                            "pacman": "Arch/Manjaro/CachyOS",
                            "yay" : "Arch",
                            "paru" : "Arch",
                            "apt": "Debian/Ubuntu/Mint",
                            "dnf": "Fedora/RHEL",
                            "zypper": "openSUSE"
                            }
                    
                        for pm, distro in managers.items():
                            if shutil.which(pm):
                                return pm, distro
                            
                        return None, None
                    
                    pm_cmd, distro = get_package_manager()
                    cmd_name = os.path.basename(pm_cmd) 
                    if cmd_name in ['yay', 'paru']:
                        rprint (f" * Found {cmd_name}")
                        rprint (f' * Trying installing and update available packages!')
                        try:
                            subprocess.run([cmd_name, '-Syu', 'python-pillow', 'python-requests', 'python-term-image', 'python-prompt_toolkit', 'python-rich', '--noconfirm'], shell=True, check=True)
                            print('\n # Installation Done! you can restart this tools!'), sys.exit()
                        except Exception as e:
                            print (f' ! {e}')
                            exit()
                    elif cmd_name == 'pacman':
                        rprint (f" * Found {cmd_name}")
                        rprint (f' * Trying installing and update available packages!')
                        try:
                            subprocess.run(['sudo', cmd_name, '-Syu', 'python-pillow', 'python-requests', 'python-term-image', 'python-prompt_toolkit', 'python-rich', '--noconfirm'], shell=True, check=True)
                            print('\n # Installation Done! you can restart this tools!'), sys.exit()
                        except Exception as e:
                            print (f' ! {e}')
                            exit()
                    elif cmd_name == 'apt':
                        rprint (f" * Found {cmd_name}")
                        rprint (f' * Trying installing and update available packages!')
                        try:
                            subprocess.run(['sudo', cmd_name, 'update', '&&', 'sudo', cmd_name, 'upgrade', '&&', 'sudo', cmd_name, 'install', 'python-requests', 'python-rich', 'python-term-image', 'python-prompt-toolkit'], shell=True, check=True)
                            print('\n # Installation Done! you can restart this tools!'), sys.exit()
                        except Exception as e:
                            print (f' {e}')
                            exit()
                    elif cmd_name == 'dnf':
                        rprint (f" * Found {cmd_name}")
                        rprint (f' * Trying installing and update available packages!')
                        try:
                            subprocess.run([cmd_name, 'install', 'python3-pillow', 'python3-requests', 'python3-rich', 'python3-prompt-toolkit'], shell=True, check=True)
                            print('\n # Installation Done! you can restart this tools!'), sys.exit()
                        except Exception as e:
                            print (f' {e}')
                            exit()
                    elif cmd_name == "zypper":
                        rprint (f" * Found {cmd_name}")
                        rprint (f' * Trying installing and update available packages!')
                        try:
                            subprocess.run(['sudo', cmd_name, 'install', 'python3-Pillow', 'python3-requests', 'python3-rich', 'python3-prompt_toolkit'], shell=True, check=True)
                            print('\n # Installation Done! you can restart this tools!'), sys.exit()
                        except Exception as e:
                            print (f' {e}')
                            exit()
                    else:
                        rprint (f' * Package manager not found or not supported!')
            
                print(" # Installation Succesfully, restart this tools!"); exit()
                
except Exception as e:
    stop_event.set()
    rprint(f"\n[bold red]![/bold red] An error occurred during import: {e}")
    sys.exit()

def loading_animation(teks):
    i = 0
    while not stop_event.is_set():
        dot = '.' * (i % 5)
        print(f"\r {teks}{dot:<5}", end='', flush=True)
        time.sleep(0.3)
        i += 1

def run_with_animation(func, teks):
    loading_thread = threading.Thread(target=loading_animation, args=(teks,))
    loading_thread.start()
    try:
        func()
    except ImportError:
        stop_event.set()
        sys.exit()
    finally:
        stop_event.set()
        loading_thread.join()
    stop_event.set()
    loading_thread.join()

try:
    run_with_animation(import_module, "[*] Importing Module")
except (KeyboardInterrupt, OSError):
    rprint("\n ! Exiting...")
    exit()

stop_event.set()

# Fungsi Rekursif
def recursive_input(mentah, extension=None):
    """
    Mencari file berdasarkan input user (file, folder, atau wildcard).
    Return: list of Path objects.
    """
    search_path = Path(mentah).expanduser()
    found_files = []

    # 1. Jika inputnya adalah file spesifik
    if search_path.is_file():
        if search_path.suffix.lower() == extension:
            found_files.append(search_path.resolve())
    
    # 2. Jika inputnya folder atau mengandung wildcard
    else:
        # Jika user kasih folder, tambahkan wildcard ke belakang
        if search_path.is_dir():
            pattern = f"**/*{extension}"
        else:
            # Jika user sudah kasih pattern (misal *.ani), pakai itu saja
            pattern = search_path.name
            search_path = search_path.parent
            
        found_files.extend(search_path.rglob(pattern))
    
    return [f.resolve() for f in found_files]

# Main tools
banner()
def main():
    console = Console()
    try:
        lists = Table(show_header=False, show_edge=False, pad_edge=False, box=None)
    
        rprint("\n[orange1] > [/orange1]Select an options.\n")
        lists.add_row("[bold green] 1 [/bold green]", "Convert", ".ani", "to", "XCur")
        lists.add_row("[bold green] 2 [/bold green]", "Convert", "XCur", "to", ".ani")
        lists.add_row("[bold green] 3 [/bold green]", "Convert", ".GIF", "to", ".ani")
        lists.add_row("[bold green] 4 [/bold green]", "Convert", ".GIF", "to", "XCur\n")
        console.print(lists)

    # Cache history
        history_file = FileHistory(os.path.join(tmp_dir, "sxcc", ".sxcc_history"))
        history_name = FileHistory(os.path.join(tmp_dir, "sxcc", ".sxcc_history_name"))

        choice = prompt(HTML("<style fg='#fdb9c0'> ? </style>Please enter your choice: ")).strip()
        mentah = prompt(HTML("<style fg='#fdb9c0'> > </style>Please enter the path to your input file or folder (Can use '~' for home directory): "), history=history_file, auto_suggest=AutoSuggestFromHistory()).strip()
        cursors_name = prompt(HTML("<style fg='#fdb9c0'> > </style>Name of Cursors: "), history=history_name, auto_suggest=AutoSuggestFromHistory()).strip()
        mentah = os.path.expanduser(mentah)
        sxcc_link = os.path.join(tmp_dir, "sxcc", "sxcc.link")

        path_jembatan = os.path.join(tmp_dir, "sxcc")

        with open (os.path.join(str(path_jembatan), "sxcc_history_name"), 'w', encoding='UTF-8') as f:
            f.write(cursors_name)

        if choice == "1":
            file_list = recursive_input(mentah, extension=".ani")
            with open (sxcc_link, 'w', encoding='UTF-8') as f:
                for path in file_list:
                    f.write(str(path) + '\n')

            if sys.platform in ["linux", "linux2"]:
                rprint("\n [black on orange1] # [/black on orange1] Extracting frames from .ani file..."); time.sleep (2)
                from Assets.Engine.extractor_ani import ekstrak
                ekstrak()

                rprint("\n [black on orange1] # [/black on orange1] Converting .cur frames to .png..."); time.sleep(2)
                from Assets.Engine.converter import convert_cur_to_png
                convert_cur_to_png()

                rprint("\n [black on orange1] # [/black on orange1] Building XCursor files..."); time.sleep(2)
                from Assets.Engine.compiler import compiler_xcur
                compiler_xcur()
            else:
                rprint("\n [black on green]*[/] This feature is currently only supported on Linux. Please check back later for updates!"); exit()

        elif choice == "2":
            rprint("\n [*] This feature is currently under development. Please check back later!")
        elif choice == "3":
            rprint("\n [*] This feature is currently under development. Please check back later!")
        elif choice == "4":
            rprint("\n [*] This feature is currently under development. Please check back later!")
        else:
            rprint("\n [*] Thank you for using Sreetx Cross Cursor! Goodbye!")
            exit()
    except (KeyboardInterrupt, EOFError):
        rprint("\n [*] Exiting..."); sys.exit()

if __name__ == "__main__":
    main()
