# SXCC
Sreetx Cross Cursor Converter! Easy to USE!

Use any type of cursor theme from anywhere!
A tool to convert Windows cursor files to run on Linux!
Let's bring your favorite waifu to the Linux world through cursors!

# Changelog

    Rewrite SXCC from zero, Verison 0.31

# Support the Project!

* **Saweria:** https://saweria.co/linggachannel

* **YouTube:** https://youtube.com/@linggachannel4781
* **PayPal:** https://paypal.me/Sreetx

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
                |--> frame_001.svg 
                |--> metadata.json
                    (the same as the structure above)

## This note very important! Please read!
The frames file must be in SVG format, it cannot be PNG, JPEG or other image files other than SVG! A structure like this looks very flexible and can be used in various distros that still use X11, hybrid, or those that use SVG completely. but in my tools the mode for creating SVG and XCUR cursors is separated so you need to run the tools twice

## metadata structures
The metadata structure should be like this:

### A. For static cursors
** Note, Don't raw copy the code below, this is just an example! The code structure is valid and why can't you just copy and paste because the description containing the "<--" sign is included in the real .json file so the code will have an error!

in metadata.json for a static cursor, just write the metadata like this:

        [
    {
        "filename": "frame_001.svg",    <-- Pay attention to the name of the frame or image 
        "hotspot_x": 0,                 <-- Hotspot X is counted from the top left to the top left (horizontal)
        "hotspot_y": 0,                 <-- Hotspot Y is counted from top left to bottom left (vertical)
        "nominal_size": 32              <-- The SVG size is mandatory and must be the same as the nominal_size so that the cursor size can be set via supported cursor settings!
        
    }
        ]

### B. For animated cursors
To create metadata.json for animated cursors, we only need to write the json code above (for static cursors) repeatedly in the same file with a note that the "filename" must not be the same so that the frame runs correctly.

    [
        {
            "filename": "frame_001.svg",    <-- Look at the numbers on the frame, they can't be the same for every block
            "delay": 100,                   <-- delay is the value of how long the delay is until the next frame is displayed. This delay is calculated in ms (milli seconds). The most appropriate number is 100ms, not too fast, not too slow
            "hotspot_x": 5,
            "hotspot_y": 2,
            "nominal_size": 32
        },
        {
            "filename": "frame_002.svg",    <-- look and compare the numbers for this frame and the one above, they are clearly different, right? and it's good to do it sequentially
            "delay": 100,
            "hotspot_x": 5,
            "hotspot_y": 2,
            "nominal_size": 32
        },
        xxx Continue here until your frame runs out / is finished... :)
        xxx
        xx
    ]

# Deps
This tool uses quite a lot of libs to run smoothly. For manual installation, you only need to install a few basic libs so that the tool can run smoothly:

1. python (arch linux) or python3 (debian/ubuntu/etc.)
2. git
3. xcursorgen
4. pip or python-pip (arch linux)

The remaining libs will be installed automatically via the SXCC tool, so there's no need to worry if there are deps problems.

# Special Thanks
Thank you for use this tools. I created this tool as a way around the problem of GNOME 51 only accepting SVG cursors and allowing Windows ANI cursors to run on SVG and XCUR Linux!
Don't forget to subscribe in my Channel!



            
        
