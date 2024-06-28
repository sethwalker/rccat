from zulip_bots.lib import ExternalBotHandler
import importlib


def dispatch(command, message, client):
    bot_handler = ExternalBotHandler(client, None, None)
    # strip the command from the message
    message["content"] = message["content"][len(command) + 2 :]

    SEND_HELP = True if "help" == command else False
    if SEND_HELP:
        command = message["content"].split(" ")[0]
        if not command:
            return bot_handler.send_reply(
                message,
                "hi, i'm @**rccat**. i can do a few things (try ?list). [add more](https://github.com/sethwalker/rccat)",
            )

    match command:
        case "list":
            if SEND_HELP:
                return bot_handler.send_reply(
                    message, "`list`: returns a list of available commands, probably"
                )
            bot_handler.send_reply(
                message,
                "help, list, convert, time, ritersay, riterscroll, scrollart, selffive",
            )
            return

        case "time":
            import dateparser

            u = client.get_user_by_id(message["sender_id"])
            tz = u["user"]["timezone"]
            t = dateparser.parse(
                message["content"],
                settings={"TIMEZONE": tz, "RETURN_AS_TIMEZONE_AWARE": True},
            )
            bot_handler.send_reply(message, "<time: {}>\n\n`<time: {}>`".format(t, t))
            return

        case "selffive":
            client.add_reaction(
                {"message_id": message["id"], "emoji_name": "highfive-pika"}
            )
            return

        case "ritersay":
            from handlers import riter

            riter.say(message["content"])
            return

        case "riterscroll":
            from handlers import riter

            riter.scroll(message["content"])
            return

        # proof of concept forwarding to other (local) zulip bots
        # TBD?: forward via chat to other external bots
        case "convert":
            from handlers.bots.converter import converter

            handler = converter.handler_class()
            if SEND_HELP:
                bot_handler.send_reply(message, handler.usage())
            else:
                handler.handle_message(message, bot_handler)

        case "scrollart":
            from handlers.scrollart import orbitaltravels

            reply = orbitaltravels.handle_message(message, bot_handler)
            bot_handler.send_reply(message, reply)
            return

        case _:
            try:
                handler = importlib.import_module("handlers.{}".format(command))
                if SEND_HELP:
                    reply = handler.usage()
                else:
                    reply = handler.handle_message(message, bot_handler)
                if reply:
                    bot_handler.send_reply(message, reply)
            except Exception as e:
                print(e)
                # TODO: if direct message or mention, otherwise ignore
                bot_handler.send_reply(message, "unknown command, try ?list")
