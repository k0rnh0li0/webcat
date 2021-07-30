#!/usr/bin/env python3
# driver.py
# K0RNH0LI0 2021
#
# Driver for BlueTooth thermal cat printers.
# Adapted from JJJollyjim/PyCatte on GitHub for
# readability and portability.

import asyncio
from bleak import BleakClient
import crcmod.predefined
import time
import os

import config

crc = crcmod.predefined.mkCrcFun("crc-8")

char = "0000ae01-0000-1000-8000-00805f9b34fb"

def revbits(b):
    # Reverse bits in a byte.
    result = 0
    for i in range(8):
        result = result | (((b >> i) & 0x01) << (7 - i))
    return result

def make_command(cmd, payload):
    assert 0 < len(payload) < 0x100

    msg = bytearray([0x51, 0x78, cmd, 0x00, len(payload), 0x00])
    msg += payload
    msg.append(crc(payload))
    msg.append(0xFF)

    return bytes(msg)

async def catprint(im, CLIENT):
    assert im[0:3] == b"P4\n", f"stdin was not a P4 PBM file, first 3 bytes: {im[0:3]}"
    im = im[3:]
    while im[0] == b"#"[0]:
        im = im[(im.index(b"\n") + 1) :]
    w, h = map(int, im[: (im.index(b"\n"))].decode("ascii").split(" "))
    assert w == 384, f"input image's width was {w}, expected 384"
    im = im[(im.index(b"\n") + 1) :]
    assert (
        len(im) == 48 * h
    ), f"input PBM file was a weird length, expected w*h/8 = {48*h}, got {len(im)}"

    buf = bytearray()

    for i in range(h):
        buf += make_command(
            0xA2, bytes(map(revbits, im[(i * 48) : ((i + 1) * 48)]))
        )

    if config.FEED_AFTER > 0:
        buf += make_command(
            0xA1, bytes([config.FEED_AFTER % 256, config.FEED_AFTER // 256])
        )

    mtu = config.MTU

    while len(buf) > mtu:
        await CLIENT.write_gatt_char(char, buf[0:mtu], True)
        buf = buf[mtu:]
        # prevent printer from tripping on itself
        #\TODO come up with a better solution
        time.sleep(0.1)

    if len(buf) > 0:
        await CLIENT.write_gatt_char(char, buf, True)

async def main():
    async with BleakClient(config.BDADDR) as client:
        while True:
            if not os.path.exists("image.pbm"):
                await asyncio.sleep(1)
                continue
            with open("image.pbm", "rb") as f:
                await catprint(f.read(), client)
                os.remove("image.pbm")

if __name__ == "__main__":
    asyncio.run(main())
