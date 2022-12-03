#!/usr/bin/env python3
import sys, json
from datetime import datetime, timezone

strtime = '%Y-%m-%d %H:%M:%S'

def load_messages(filename):
    """Load the messages json dump."""
    with open(filename) as dump: return json.load(dump)

def author(message):
    """Return the author (its username) of a message."""
    return message['author']['username']

def content(message):
    """Return the content of a message."""
    return message['content']

def timestamp(message):
    """Return the timestamp (in localtime) of a message."""
    utc = datetime.fromisoformat(message['timestamp'])
    local = utc.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return local.strftime(f'[{strtime}]')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: ./{sys.argv[0]} messages.json", file=sys.stderr)
        exit(1)
    for m in reversed(load_messages(sys.argv[1])):
        print(f'{timestamp(m)} {author(m)}: {content(m)}')
