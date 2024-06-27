from zulip_bots.lib import ExternalBotHandler
import importlib


def dispatch(command, message, client):
    bot_handler = ExternalBotHandler(client, None, None)
    # strip the command from the message
    message["content"] = message["content"][len(command) + 1 :]

    match command:
        case "help":
            bot_handler.send_reply(message, "you have now been helped")
            return

        case "list":
            bot_handler.send_reply(
                message,
                "help, list, convert, time, ritersay, riterscroll, scrollart, selffive",
            )

        case "time":
            import dateparser

            u = client.get_user_by_id(message["sender_id"])
            tz = u["user"]["timezone"]
            t = dateparser.parse(
                message["content"],
                settings={"TIMEZONE": tz, "RETURN_AS_TIMEZONE_AWARE": True},
            )
            bot_handler.send_reply(message, "<time: {}>\n\n`<time: {}>`".format(t, t))

        case "selffive":
            client.add_reaction(
                {"message_id": message["id"], "emoji_name": "highfive-pika"}
            )

        case "ritersay":
            from handlers import riter

            riter.say(message["content"])

        case "riterscroll":
            from handlers import riter

            riter.scroll(message["content"])

        # proof of concept forwarding to other (local) zulip bots
        # TBD?: forward via chat to other external bots
        case "convert":
            from handlers.bots.converter import converter

            handler = converter.handler_class()
            handler.handle_message(message, bot_handler)

        case "scrollart":
            from handlers.scrollart import orbitaltravels

            reply = orbitaltravels.handle_message(message, bot_handler)
            bot_handler.send_reply(message, reply)

        case _:
            try:
                handler = importlib.import_module("handlers.{}".format(command))
                reply = handler.handle_message(message, bot_handler)
                if reply:
                    bot_handler.send_reply(message, reply)
            except Exception as e:
                print(e)
                # TODO: if direct message or mention, otherwise ignore
                bot_handler.send_reply(message, "unknown command, try ?list")
