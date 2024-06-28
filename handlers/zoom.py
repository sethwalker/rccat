def usage():
    return "you have been zoomed"


def handle_message(message, bot_handler):
    room = message["content"].split(" ")[0]

    # TODO
    # if no room, join the meeting on your calendar
    # if no meeting, pick a random available room
    # handle the pairing stations

    bot_handler.send_reply(
        message,
        f"Zoom link: [{room.title()}](https://www.recurse.com/zoom/{room.lower()})",
    )
