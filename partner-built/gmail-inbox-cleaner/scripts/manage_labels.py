#!/usr/bin/env python3
"""
Create, list, and look up Gmail labels.

Usage:
    python3 manage_labels.py --token token.json list
    python3 manage_labels.py --token token.json create --name "Receipts"
    python3 manage_labels.py --token token.json get-id --name "Finance"
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gmail_service import get_service


def list_labels(service):
    result = service.users().labels().list(userId="me").execute()
    user_labels = [l for l in result.get("labels", []) if l.get("type") == "user"]
    system_labels = [l for l in result.get("labels", []) if l.get("type") == "system"]

    print(f"\nUser labels ({len(user_labels)}):")
    for l in sorted(user_labels, key=lambda x: x["name"]):
        print(f"  {l['id']:45s}  {l['name']}")

    print(f"\nSystem labels ({len(system_labels)}):")
    for l in sorted(system_labels, key=lambda x: x["name"]):
        print(f"  {l['id']:45s}  {l['name']}")

    return {l["name"]: l["id"] for l in result.get("labels", [])}


def create_label(service, name):
    # Check if already exists
    result = service.users().labels().list(userId="me").execute()
    for l in result.get("labels", []):
        if l["name"].lower() == name.lower():
            print(f"Label already exists: '{l['name']}' → {l['id']}")
            return l["id"]

    label = service.users().labels().create(
        userId="me",
        body={
            "name": name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show",
        }
    ).execute()
    print(f"Created label: '{label['name']}' → {label['id']}")
    return label["id"]


def get_label_id(service, name):
    result = service.users().labels().list(userId="me").execute()
    for l in result.get("labels", []):
        if l["name"].lower() == name.lower():
            print(f"{l['id']}")
            return l["id"]
    print(f"Label not found: '{name}'")
    return None


def main():
    parser = argparse.ArgumentParser(description="Manage Gmail labels.")
    parser.add_argument("--token", required=True, help="Path to OAuth token JSON")
    parser.add_argument("command", choices=["list", "create", "get-id"])
    parser.add_argument("--name", help="Label name (for create and get-id)")
    args = parser.parse_args()

    service = get_service(args.token)

    if args.command == "list":
        list_labels(service)
    elif args.command == "create":
        if not args.name:
            print("ERROR: --name required for create")
            sys.exit(1)
        create_label(service, args.name)
    elif args.command == "get-id":
        if not args.name:
            print("ERROR: --name required for get-id")
            sys.exit(1)
        get_label_id(service, args.name)


if __name__ == "__main__":
    main()
