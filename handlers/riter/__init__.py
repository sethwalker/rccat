from pythonosc import udp_client
from pathlib import Path
import subprocess
from PIL import Image


def rite(leds):
    ip = "10.100.7.28"
    port = 12000
    client = udp_client.SimpleUDPClient(ip, port)
    return client.send_message("/rccat", leds)


def say(text):
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
    return rite("".join(pixels))
