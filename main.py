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
            import ffmpeg

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
                rprint(" * Installing packages...")
                if sys.platform in ["win32", "win"]:
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "rich", "prompt_toolkit", "term-image", "pillow", "ffmpeg-python"], check=True)
                        print(f"\n # Packages installed successfully! Please restart the program."); exit()
                if sys.platform in ["linux", "linux2"]:
                    print(" ! Auto installation with pip falied! Trying to install with system package manager..."); time.sleep(2)
                    try:
                        subprocess.run(["sudo", "pacman", "-Syu"])
                    except subprocess.CalledProcessError:
                        try:
                            print(f"\n # Installing Components (APT)..."); time.sleep(0.3)
                            subprocess.run(['sudo', 'apt', 'update', '&&', 'sudo', 'apt', 'upgrade'], shell=True)
                            subprocess.run(['sudo', 'apt', 'install', 'python3-requests', 'python3-prompt_toolkit', 'python3-rich', 'python3-term-image', 'python3-pillow'], shell=True)
                            print(f"\n # If the installation error occurs, you can install it manually")
                            for i, h in enumerate(['Requests', 'Prompt Toolkit', 'Rich', 'Pillow', 'Term-Image'], 1): 
                                print(f" {i}. {h}")

                            print (f"\n # Components installation successfuly")
                            print (f" # You can use this tools btw"); time.sleep(0.4)
                            exit()
                        except subprocess.CalledProcessError:
                            print (f"\n ! APT or Pacman package manager is not working properly! Please install the required packages manually and restart the program."); exit()

                    paru = shutil.which("paru")
                    yay = shutil.which("yay")
                    if paru and yay:
                        print (f"\n * Many AUR helper found!")
                        for i, h in enumerate(['paru', 'yay'], 1): 
                            print(f" {i}. {h}")
                        
                        choice = str(input(f" ? Choose one: "))
                        if choice.lower() == "1":
                            helper = paru
                        elif choice.lower() == "2":
                            helper = yay
                        else:
                            print(f" # Please select one!")
                            exit()
                    elif paru:
                        helper = paru
                    elif yay:
                        helper = yay
                        
                    else:
                        print(f"\n ! AUR helper not found! please install yay or paru")

                    helper_list = helper.split('/')[-1]

                    print(f"\n # Installing Components ({helper_list})..."); time.sleep(0.3)
                    try:
                        subprocess.run([helper, '-S', 'python-requests', 'python-rich', 'python-prompt_toolkit', 'python-term-image', 'python-pillow', '--noconfirm'], check=True)
                    except Exception as e:
                        print(f" ! Something went wrong!")
                        print(e)
                        exit()
                        rprint (" * Checking for xcursorgen dependency..."); time.sleep(1)

                    if not shutil.which("xcursorgen"):
                        managers = {
                            "pacman": "xorg-xcursorgen",
                            "apt-get": "x11-apps",
                            "dnf": "xcursorgen",
                            "zypper": "xcursorgen"
                            }
                        found_pm = None
                        package_to_install = None
                        for pm, pkg in managers.items():
                            if shutil.which(pm):
                                found_pm = pm
                                package_to_install = pkg
                                break

                        cmd = ["sudo", found_pm]
                            
                        if found_pm == "pacman":
                            cmd.extend(["-S", "--noconfirm", package_to_install])
                        elif found_pm == "apt-get":
                            subprocess.run(["sudo", "apt-get", "update"], check=True)
                            cmd.extend(["install", "-y", package_to_install])
                        else:
                            print (f"\n ! Xcursorgen auto installation is only supported on Pacman and APT package manager! Please install xcursorgen manually and restart the program."); time.sleep(2)

                        try:
                            subprocess.run(cmd, check=True)
                        except subprocess.CalledProcessError as e:
                            rprint(f"[white on red] FAIL [/] Error installing {package_to_install}: {e}")
                        rprint(f"SUCCESS {package_to_install} is installed and ready to use!"); exit()
                    else:
                        pass
                else:
                    print(f"\n ! Automatic installation is only supported on Linux! Please install the required packages manually and restart the program.")
                    print(f" ! Required packages: rich, pillow, prompt_toolkit, term-image, ffmpeg-python")
                    exit()

                rprint(" * Packages installed successfully! Please restart the program."); exit()
            else: 
                rprint(" (*) Cannot run the program without installing the required packages. Exiting.")
                exit()
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
        mentah = prompt(HTML("<style fg='#fdb9c0'> > </style>Please enter the path to your input file (Can use '~' for home directory): "), history=history_file, auto_suggest=AutoSuggestFromHistory()).strip()
        cursors_name = prompt(HTML("<style fg='#fdb9c0'> > </style>Name of Cursors: "), history=history_name, auto_suggest=AutoSuggestFromHistory()).strip()
        mentah = os.path.expanduser(mentah)

        path_jembatan = os.path.join(tmp_dir, "sxcc")
        with open (os.path.join(str(path_jembatan), "sxcc.link"), 'w', encoding='UTF-8') as f:
            f.write(mentah)

        with open (os.path.join(str(path_jembatan), "sxcc_history_name"), 'w', encoding='UTF-8') as f:
            f.write(cursors_name)

        if choice == "1":
            if sys.platform in ["linux", "linux2"]:
                rprint("\n [black on orange1] # [/black on orange1] Extracting frames from .ani file..."); time.sleep (2)
                from Assets.Engine.extractor_ani import ekstrak
                ekstrak()

                rprint("\n [black on orange1] # [/black on orange1] Converting .cur frames to .png...\n"); time.sleep(2)
                from Assets.Engine.converter import convert_cur_to_png
                convert_cur_to_png()

                rprint("\n [black on orange1] # [/black on orange1] Building XCursor files...\n"); time.sleep(2)
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