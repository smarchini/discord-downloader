#!/usr/bin/env python3
import sys, json, requests
from datetime import datetime, timezone

strtime = '%Y-%m-%d %H:%M:%S'

def get_request(url, headers, params):
    """Perform a get request and return a json deserialized into an object."""
    return json.loads(requests.get(url, headers=headers, params=params).content)

def parse_localtime(timestamp):
    """Parse a localtime timestamp (as printed by discord-chatlog.py)"""
    return datetime.strptime(timestamp, strtime).replace(tzinfo=None);

def parse_utctime(timestamp):
    """Parse an utctime timestamp (as printed by Discord API)"""
    return datetime.fromisoformat(timestamp).replace(tzinfo=None);

def fetch_all_messages(auth_token, channel_id, begin):
    """https://discord.com/developers/docs/resources/channel#get-channel-messages"""
    url = f"http://canary.discordapp.com/api/channels/{channel_id}/messages"
    headers = { "authorization": auth_token }
    messages = get_request(url, headers, {"limit": 100}) # can't fetch more than 100
    while last := get_request(url, headers, {"limit": 100, "before" : messages[-1]['id']}):
        if parse_utctime(messages[-1]['timestamp']) <= begin: break
        messages += last
    return [ m for m in messages if parse_utctime(m['timestamp']) > begin ]

if __name__ == '__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print(f"Usage: ./{sys.argv[0]} auth_token channel_id ({strtime})", file=sys.stderr)
        exit(1)
    begin = parse_localtime(sys.argv[3]) if sys.argv[3] else datetime.min
    json.dump(fetch_all_messages(sys.argv[1], sys.argv[2], begin), sys.stdout)
