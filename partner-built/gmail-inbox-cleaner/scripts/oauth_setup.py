#!/usr/bin/env python3
"""
OAuth token setup — dual scope (gmail.modify + gmail.settings.basic).

The sandbox localhost is unreachable from the user's browser, so the
standard local-server redirect flow doesn't work. This script generates
the auth URL. Claude in Chrome navigates to it, the user clicks Allow,
Chrome redirects to localhost (shows "connection refused" — expected),
and Claude reads the auth code from the tab URL via tabs_context_mcp.

Usage:
    python3 oauth_setup.py --credentials /path/to/credentials.json --token /path/to/token.json
"""
import argparse
import json
import secrets
import urllib.parse
import requests

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.settings.basic",
]
REDIRECT_URI = "http://localhost"
TOKEN_URI = "https://oauth2.googleapis.com/token"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"


def load_credentials(path):
    with open(path) as f:
        data = json.load(f)
    installed = data.get("installed") or data.get("web", {})
    return installed["client_id"], installed["client_secret"]


def generate_auth_url(client_id):
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "state": secrets.token_urlsafe(16),
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "false",
    }
    return AUTH_URI + "?" + urllib.parse.urlencode(params)


def exchange_code(code, client_id, client_secret):
    resp = requests.post(TOKEN_URI, data={
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    })
    resp.raise_for_status()
    return resp.json()


def save_token(token_data, client_id, client_secret, path):
    token_data["client_id"] = client_id
    token_data["client_secret"] = client_secret
    token_data["token_uri"] = TOKEN_URI
    token_data["scopes"] = SCOPES
    with open(path, "w") as f:
        json.dump(token_data, f, indent=2)
    print(f"Token saved to: {path}")
    print(f"Scopes: {SCOPES}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up Gmail OAuth token with dual scopes.")
    parser.add_argument("--credentials", required=True, help="Path to credentials.json from Google Cloud Console")
    parser.add_argument("--token", required=True, help="Output path for token.json")
    parser.add_argument("--code", help="Auth code (if already captured from browser URL bar)")
    args = parser.parse_args()

    client_id, client_secret = load_credentials(args.credentials)

    if args.code:
        token_data = exchange_code(args.code, client_id, client_secret)
        save_token(token_data, client_id, client_secret, args.token)
    else:
        url = generate_auth_url(client_id)
        print("\nOpen this URL in your browser:")
        print(url)
        print("\nAfter clicking Allow, the browser will show 'connection refused' — that is expected.")
        print("The auth code is in the URL bar. Run this script again with --code <code> to complete setup.")
