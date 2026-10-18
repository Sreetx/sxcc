# SXCC
Sreetx Cross Cursor Converter! Easy to USE!

Use any type of cursor theme from anywhere!
With this tool you can convert .ani (Windows) files to XCurosrs (Linux) which can be used in linux!
Let's bring your favorite waifu to the Linux world through cursors!

# Changelog

    Rewrite SXCC from zero, Verison 0.31

# Support the Project!

* **Saweria:** https://saweria.co/linggachannel

* **YouTube:** https://youtube.com/@linggachannel4781

# Installation

For Linux Distro:

    curl -sSL https://raw.githubusercontent.com/Sreetx/sxcc/refs/heads/master/install.sh | sh

Run Tools!

    sxcc

For non-Linux distro:

    git clone https://github.com/Sreetx/sxcc.git
    cd sxcc
    python3 main.py

# Compability

Can run on Linux, Android (Termux), and Windows (Eksperimental)

For automatic installation via other than pacman it is the EXPERIMENTAL period!

# Deps

Dependencies will be installed automatically when you run the tool. For operating systems that aren't automatically installed, please install them manually!

1. Python
2. Python-pillow
3. Python-rich
4. Python-prompt_toolkit
5. Python-term-image
6. Python-clickgen

## NEW INFO!
GNOME 51+ and Plasma 6.14+ start implementing SVG cursors as the default option, the structure is something like this:

        Skirk Cursors (examples)
        |
        |--> Index.theme
        |--> Cursors
        |   |--> normal
        |   |--> default, xxx (for X11 / Xcur Cursors)
        |--> cursors_scalable
            |--> normal (this all is folder)
            |   |--> frame_001.svg
            |   |--> metadata.json
            |--> hand (this is folder too)
            
        
