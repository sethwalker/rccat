import zulip
from multiprocessing import Process
import subprocess


def main():
    client = zulip.Client(config_file="zuliprc")
    client.call_on_each_message(lambda message: run(message, client))


def run(message, client):
    p = Process(target=handle_message, args=(message, client))
    p.start()
    p.join()


def handle_message(message, client):
    if "!update" == message["content"]:
        u = client.get_user_by_id(message["sender_id"])
        if can_update(u["user"]):
            update(client)
        return

    if (
        message["content"].startswith("?")
        or message["content"].startswith("@**rccat** ?")
        or message["content"].startswith("@**rccat-dev** ?")
    ):
        words = (
            message["content"]
            .lstrip("@**rccat** ")
            .lstrip("@**rccat-dev** ")
            .split(" ")
        )
        command: str = words[0]

        from dispatcher import dispatch

        dispatch(command.lstrip("?"), message, client)

    else:
        print("not a command")
        print(message)


def can_update(user):
    return "seth.h.walker@gmail.com" == user["email"]


def update(client):
    git_output = subprocess.check_output(["git", "pull"], text=True)
    pip_output = subprocess.check_output(
        ["pip", "install", "-r", "requirements.txt"], text=True
    )
    message_content = "`git pull`\n```sh\n{}```\n`pip install -r requirements.txt`\n```sh\n{}```".format(
        git_output, pip_output
    )
    reply = {
        "type": "stream",
        "to": "test-bot",
        "topic": "rccat",
        "content": message_content,
    }
    client.send_message(reply)
    print(message_content)

    return message_content


if __name__ == "__main__":
    main()
