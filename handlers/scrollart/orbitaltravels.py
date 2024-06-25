import random, math

EMPTY = " "

CHARS = []
SINE_STEP_INCS = []
sine_steps = []
for i in range(random.randint(7, 15)):
    CHARS.append(random.choice("@O0o*.,vV"))
    SINE_STEP_INCS.append(random.random() * 0.1 + 0.0001)
    sine_steps.append(random.random() * math.pi)

WIDTH = 96  # os.get_terminal_size()[0] - 1


def handle_message(message, bot_handler):
    reply = ["```"]
    for line in range(38):
        row = [EMPTY] * WIDTH

        for i in range(len(CHARS)):
            row[int((math.sin(sine_steps[i]) + 1) / 2 * WIDTH)] = CHARS[i]
            sine_steps[i] += SINE_STEP_INCS[i]

        reply.append("".join(row))

    reply.append("```")
    reply.append("Helix Travels, by Al Sweigart al@inventwithpython.com 2024")
    return "\n".join(reply)
