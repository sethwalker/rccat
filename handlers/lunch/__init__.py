import sqlite3
from pathlib import Path


def handle_message(message, bot_handler):
    DB_PATH = Path(__file__) / Path("../locations.db")
    print("connecting to lunch locations db", DB_PATH)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    res = cur.execute(
        "SELECT name, url, description FROM restaurants ORDER BY RANDOM() LIMIT 1"
    )
    return "\t".join(res.fetchone())
