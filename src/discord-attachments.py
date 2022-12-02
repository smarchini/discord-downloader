#!/usr/bin/env python3
import sys, json

def load_messages(filename):
    """Load the messages json dump."""
    with open(filename) as dump: return json.load(dump)

def authors(messages):
    """Return the set of authors: (username, id)."""
    return set((m['author']['username'], m['author']['id']) for m in messages)

def flatten(lst):
    """Transform a list of lists to plain list."""
    return [item for sublist in lst for item in sublist]

def attachments_urls(messages, author_id):
    """Return all the attachments (the url) sent by an author."""
    attachments = flatten(m['attachments'] for m in messages
                          if m['author']['id'] == author_id and m['attachments'])
    return set(a['url'] for a in attachments)

if __name__ == '__main__':
    messages = load_messages(sys.argv[1]) if len(sys.argv) >= 2 else []
    if len(sys.argv) != 3:
        print(f"Usage: ./{sys.argv[0]} messages.json author_id", file=sys.stderr)
        for (user, id) in authors(messages): print(f"- {user}: {id}", file=sys.stderr)
        exit(1)
    for url in attachments_urls(messages, sys.argv[2]): print(url)
