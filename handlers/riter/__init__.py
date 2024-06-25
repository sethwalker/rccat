from pythonosc import udp_client
from pathlib import Path
import subprocess
from PIL import Image
from itertools import batched
from collections import deque
import time

DELAY = 0.1


def rite(leds):
    ip = "10.100.7.28"
    port = 12000
    client = udp_client.SimpleUDPClient(ip, port)
    return client.send_message("/rccat", leds)


def scroll(text, times=5):
    leds = greg_say(text)
    lines = list(map(deque, batched(leds, 96)))

    for i in range(times):
        for j in range(96):
            for line in lines:
                line.rotate(1)

            rite("".join(["".join(line) for line in lines]))
            time.sleep(DELAY)


def say(text):
    return rite(greg_say(text))


def greg_say(text):
    FONT_PATH = Path(__file__) / Path("../font-undead-pixel-8.ttf")
    TMP_OUT_PATH = Path("/tmp/out.png")

    subprocess.run(
        [
            "convert",
            "-background",
            "black",
            "-fill",
            "white",
            "-size",
            "96x38",
            "-pointsize",
            "8",
            "-font",
            # absolute path to font
            FONT_PATH.resolve(),
            f"caption:{text}",
            "/tmp/out.png",
        ]
    )

    im = Image.open(TMP_OUT_PATH)
    pixels = ["1" if pixel else "0" for pixel in im.getdata()]
    return "".join(pixels)
