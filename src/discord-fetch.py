#!/usr/bin/env python3
import sys, json, requests

def get_request(url, headers, params):
    """Perform a get request and return a json deserialized into an object."""
    return json.loads(requests.get(url, headers=headers, params=params).content)

def fetch_all_messages(auth_token, channel_id):
    """https://discord.com/developers/docs/resources/channel#get-channel-messages"""
    url = f"http://canary.discordapp.com/api/channels/{channel_id}/messages"
    headers = { "authorization": auth_token }
    messages = get_request(url, headers, {"limit": 100}) # can't fetch more than 100
    while last := get_request(url, headers, {"limit": 100, "before" : messages[-1]['id']}):
        messages += last
    return messages

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: ./{sys.argv[0]} auth_token channel_id", file=sys.stderr)
        exit(1)
    json.dump(fetch_all_messages(sys.argv[1], sys.argv[2]), sys.stdout)
