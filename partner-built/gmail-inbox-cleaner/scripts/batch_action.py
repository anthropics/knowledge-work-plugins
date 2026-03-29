#!/usr/bin/env python3
"""
Batch action on Gmail messages — trash, archive, label, restore, or mark read.

Usage:
    python3 batch_action.py --token token.json --action trash --ids-file ids.json
    python3 batch_action.py --token token.json --action label --label-id Label_XXX --ids-file ids.json
    python3 batch_action.py --token token.json --action mark-read --ids-file ids.json
    python3 batch_action.py --token token.json --action restore --ids-file ids.json

ids.json should be a JSON array of Gmail message ID strings.
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gmail_service import get_service

CHUNK_SIZE = 1000  # Gmail batchModify limit


def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def trash(service, ids):
    for c in chunk(ids, CHUNK_SIZE):
        service.users().messages().batchModify(
            userId="me",
            body={"ids": c, "addLabelIds": ["TRASH"], "removeLabelIds": ["INBOX"]}
        ).execute()
        time.sleep(0.2)
    print(f"Trashed {len(ids)} messages")


def archive(service, ids):
    for c in chunk(ids, CHUNK_SIZE):
        service.users().messages().batchModify(
            userId="me",
            body={"ids": c, "removeLabelIds": ["INBOX"]}
        ).execute()
        time.sleep(0.2)
    print(f"Archived {len(ids)} messages")


def label(service, ids, label_id, skip_inbox=True):
    action = {"addLabelIds": [label_id]}
    if skip_inbox:
        action["removeLabelIds"] = ["INBOX"]
    for c in chunk(ids, CHUNK_SIZE):
        service.users().messages().batchModify(userId="me", body={"ids": c, **action}).execute()
        time.sleep(0.2)
    print(f"Labeled {len(ids)} messages → {label_id}")


def mark_read(service, ids):
    for c in chunk(ids, CHUNK_SIZE):
        service.users().messages().batchModify(
            userId="me",
            body={"ids": c, "removeLabelIds": ["UNREAD"]}
        ).execute()
        time.sleep(0.2)
    print(f"Marked {len(ids)} messages as read")


def restore(service, ids, label_id=None):
    add = ["INBOX"] + ([label_id] if label_id else [])
    for c in chunk(ids, CHUNK_SIZE):
        service.users().messages().batchModify(
            userId="me",
            body={"ids": c, "removeLabelIds": ["TRASH"], "addLabelIds": add}
        ).execute()
        time.sleep(0.2)
    print(f"Restored {len(ids)} messages to inbox")


def main():
    parser = argparse.ArgumentParser(description="Batch action on Gmail messages.")
    parser.add_argument("--token", required=True, help="Path to OAuth token JSON")
    parser.add_argument("--action", required=True,
                        choices=["trash", "archive", "label", "mark-read", "restore"],
                        help="Action to perform")
    parser.add_argument("--ids-file", required=True, help="JSON file containing list of message IDs")
    parser.add_argument("--label-id", help="Label ID (required for --action label, optional for restore)")
    parser.add_argument("--keep-in-inbox", action="store_true",
                        help="For label action: keep in inbox (don't set skip-inbox)")
    args = parser.parse_args()

    with open(args.ids_file) as f:
        ids = json.load(f)

    if not ids:
        print("No message IDs provided.")
        return

    service = get_service(args.token)
    print(f"Action: {args.action} on {len(ids)} messages")

    if args.action == "trash":
        trash(service, ids)
    elif args.action == "archive":
        archive(service, ids)
    elif args.action == "label":
        if not args.label_id:
            print("ERROR: --label-id required for label action")
            sys.exit(1)
        label(service, ids, args.label_id, skip_inbox=not args.keep_in_inbox)
    elif args.action == "mark-read":
        mark_read(service, ids)
    elif args.action == "restore":
        restore(service, ids, label_id=args.label_id)


if __name__ == "__main__":
    main()
