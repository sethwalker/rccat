import zulip
from zulip_bots.lib import ExternalBotHandler


def dispatch(command, message, bot_handler):
    # strip the command from the message
    message["content"] = message["content"][len(command) + 1 :]

    match command:
        case "help":
            bot_handler.send_reply(message, "you have been helped")
            return

        case "list":
            bot_handler.send_reply(message, "help, list, convert")

        # proof of concept forwarding to other (local) zulip bots
        # TBD?: forward via chat to other external bots
        case "convert":
            from handlers.bots.converter import converter

            handler = converter.handler_class()
            handler.handle_message(message, bot_handler)

        case _:
            # TODO: if direct message or mention, otherwise ignore
            bot_handler.send_reply(message, "unknown command, try ?list")


if __name__ == "__main__":
    client = zulip.Client(config_file="zuliprc")
    bot_handler = ExternalBotHandler(client, None, None)

    def handle_message(message):
        if message["content"].startswith("?"):
            words = message["content"].split(" ")
            command: str = message["content"].split(" ")[0]
            dispatch(command.lstrip("?"), message, bot_handler)
        else:
            print("not a command")
            print(message)

    client.call_on_each_message(handle_message)
