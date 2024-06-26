import zulip
from multiprocessing import Process
import subprocess
import importlib
import dispatcher

if __name__ == "__main__":
    client = zulip.Client(config_file="zuliprc")

    def handle_message(message):
        if "!update" == message["content"]:

            def can_update(user):
                return "seth.h.walker@gmail.com" == user["email"]

            def update():
                output = subprocess.check_output(["git", "pull"], text=True)
                reply = {
                    "type": "stream",
                    "to": "test-bot",
                    "topic": "rccat",
                    "content": "`git pull`\n```sh\n{}```".format(output),
                }
                client.send_message(reply)
                print(output)

                importlib.reload(dispatcher)

                return output

            u = client.get_user_by_id(message["sender_id"])
            if can_update(u["user"]):
                update()

            return

        if message["content"].startswith("?"):
            words = message["content"].split(" ")
            command: str = message["content"].split(" ")[0]

            from dispatcher import dispatch

            p = Process(target=dispatch, args=(command.lstrip("?"), message, client))
            p.start()
            p.join()
        else:
            print("not a command")
            print(message)

    client.call_on_each_message(handle_message)
