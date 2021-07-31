# webcat
A web interface for conveniently printing images on BlueTooth thermal cat printers.

I can't guarantee this will work on all cat printers, but [this is the one I'm using](https://www.amazon.com/dp/B08YJXLZN1).

This program is Free Software, licensed under the terms of the GNU GPLv2. See LICENSE.txt for details.

### Setup

Windows is not supported by this project, only GNU/Linux.

1. Clone this repository and `cd` into it.
2. Install Python requirements: `sudo python3 -m pip install -r requirements.txt`.
3. Install imagemagick using your distro's package manager.
4. Turn your printer on so it's discoverable.
5. Edit `src/config.py` as necessary, especially to set `BDADDR` to your printer's bluetooth address.
6. `cd` into the `src/` directory.
7. Run the printer driver: `./driver.py &` (might need root, I did on Raspbian but not on Arch).
8. Lastly, launch the web server: `./webcat.py &`.

Then you will be able to navigate to `http://localhost:<PORT>` in your browser and print images.
