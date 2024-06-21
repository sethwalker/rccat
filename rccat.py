import zulip
from zulip_bots import lib


def handle_message(message, bot_handler):
    if message["content"].startswith("?"):
        words = message["content"].split(" ")
        command: str = message["content"].split(" ")[0]
        dispatch(command.lstrip("?"), message, bot_handler)
    else:
        print("not a command")
        print(message)


def dispatch(command, message, bot_handler):
    # strip the command from the message
    message["content"] = message["content"][len(command) + 1 :]

    match command:
        case "help":
            bot_handler.send_reply(message, "you have been helped")
            return
        case "convert":
            from handlers.bots.converter import converter

            handler = converter.handler_class()
            handler.handle_message(message, bot_handler)


if __name__ == "__main__":
    client = zulip.Client(config_file="zuliprc")
    bot_handler = lib.ExternalBotHandler(client, None, None)
    client.call_on_each_message(lambda msg: handle_message(msg, bot_handler))
