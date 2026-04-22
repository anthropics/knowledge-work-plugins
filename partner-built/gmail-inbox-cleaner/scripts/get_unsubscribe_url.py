#!/usr/bin/env python3
"""
Extract unsubscribe URL from a Gmail message.

Checks List-Unsubscribe header first (most reliable).
Falls back to extracting all hrefs from the raw HTML body.

Usage:
    python3 get_unsubscribe_url.py --token token.json --message-id MSG_ID
    python3 get_unsubscribe_url.py --token token.json --sender "sender@domain.com" --index sender_index.json
"""
import argparse
import base64
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gmail_service import get_service


def get_unsubscribe_from_header(service, message_id):
    """Extract HTTP unsubscribe URL from List-Unsubscribe header."""
    msg = service.users().messages().get(
        userId="me", id=message_id, format="metadata",
        metadataHeaders=["List-Unsubscribe", "List-Unsubscribe-Post"]
    ).execute()
    headers = {h["name"].lower(): h["value"]
               for h in msg.get("payload", {}).get("headers", [])}
    unsub = headers.get("list-unsubscribe", "")
    post = headers.get("list-unsubscribe-post", "")
    urls = re.findall(r"<(https?://[^>]+)>", unsub)
    return urls[0] if urls else None, bool(post)


def get_hrefs_from_body(service, message_id):
    """Extract all hrefs from the HTML body when List-Unsubscribe header is absent."""
    msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()

    def extract_html(payload):
        parts = []
        if payload.get("mimeType") == "text/html":
            data = payload.get("body", {}).get("data", "")
            if data:
                parts.append(base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore"))
        for part in payload.get("parts", []):
            parts.extend(extract_html(part))
        return parts

    all_hrefs = []
    for html in extract_html(msg.get("payload", {})):
        all_hrefs.extend(re.findall(r'href=["\']([^"\']+)["\']', html))
    return all_hrefs


def find_message_id_for_sender(sender_email, index_path):
    with open(index_path) as f:
        index = json.load(f)
    for s in index["senders"]:
        if s["email"].lower() == sender_email.lower():
            return s["messages"][0]["id"] if s["messages"] else None
    return None


def main():
    parser = argparse.ArgumentParser(description="Get unsubscribe URL from a Gmail message.")
    parser.add_argument("--token", required=True, help="Path to OAuth token JSON")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--message-id", help="Gmail message ID")
    group.add_argument("--sender", help="Sender email address (looks up most recent message from sender_index.json)")
    parser.add_argument("--index", default="sender_index.json", help="Path to sender_index.json (used with --sender)")
    args = parser.parse_args()

    service = get_service(args.token)

    if args.sender:
        message_id = find_message_id_for_sender(args.sender, args.index)
        if not message_id:
            print(f"No messages found for sender: {args.sender}")
            sys.exit(1)
        print(f"Using most recent message from {args.sender}: {message_id}")
    else:
        message_id = args.message_id

    # Try header first
    url, has_post = get_unsubscribe_from_header(service, message_id)
    if url:
        print(f"\nList-Unsubscribe URL found:")
        print(f"  {url}")
        if has_post:
            print(f"  (one-click POST supported via List-Unsubscribe-Post header)")
        print(f"\nMethod: {'POST' if has_post else 'GET'}")
    else:
        print("\nNo List-Unsubscribe header found. Extracting hrefs from HTML body...")
        hrefs = get_hrefs_from_body(service, message_id)
        unsub_candidates = [h for h in hrefs
                            if any(kw in h.lower() for kw in ["unsubscribe", "optout", "opt-out", "manage-preferences"])]
        print(f"\nAll hrefs ({len(hrefs)} total):")
        for h in hrefs[-10:]:  # show last 10 — unsubscribe link is usually near the end
            print(f"  {h}")
        if unsub_candidates:
            print(f"\nLikely unsubscribe URLs:")
            for h in unsub_candidates:
                print(f"  {h}")
        print("\nMethod: Manual review required — navigate to URL in browser")


if __name__ == "__main__":
    main()
