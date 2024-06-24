An [irccat](https://github.com/RJ/irccat)-like for Zulip.

`@rccat` listens for `?`-prefixed keywords in direct messages streams it is subscribed to, such as:

```
?weather 11201
```

It is a design goal to make adding new keyword match patterns _very_ easy - currently they can be added to the `match` statement in the `dispatch` function in `rccat.py`. Plugin system TBD, but should at a minimum support Zulip bots that could be run via [`zulip-run-bot`](https://zulip.com/api/running-bots).

irccat is so named because in addition to reponding _within_ the chat network, one can also "cat" (usually `netcat` / `nc`) messages _into_ the chat network, for example

```sh
echo "#checkins>Seth+Walker Finished impossible stuff day with a [silly little tcp listener](https://github.com/sethwalker/rccat) that sends messages to zulip." | nc cat.recurse.com 12345
```

Newer implementations also support HTTP.
