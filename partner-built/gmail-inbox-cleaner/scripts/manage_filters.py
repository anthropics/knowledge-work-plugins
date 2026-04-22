#!/usr/bin/env python3
"""
Create, list, backup, audit, and delete Gmail filters.
Requires gmail.settings.basic OAuth scope.

Usage:
    python3 manage_filters.py --token token.json list
    python3 manage_filters.py --token token.json backup --output filters_backup.json
    python3 manage_filters.py --token token.json audit
    python3 manage_filters.py --token token.json create --from "sender1@example.com sender2.com" --label-id Label_XXX [--skip-inbox] [--mark-read]
    python3 manage_filters.py --token token.json delete --filter-id ANe1BmjXXX
    python3 manage_filters.py --token token.json delete-all  # DESTRUCTIVE — always backup first
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gmail_service import get_service

# Gmail system category label IDs — filters that only set these are "ghost" filters
SYSTEM_CATEGORY_LABELS = {
    "CATEGORY_PROMOTIONS", "CATEGORY_SOCIAL", "CATEGORY_UPDATES",
    "CATEGORY_FORUMS", "CATEGORY_PERSONAL",
}
# Actions that do nothing meaningful on their own (no routing, no user label)
INERT_ACTIONS_ONLY = {"markImportant", "neverMarkSpam", "star", "markRead"}


def list_filters(service):
    result = service.users().settings().filters().list(userId="me").execute()
    filters = result.get("filter", [])
    print(f"\n{len(filters)} filters:\n")
    for i, f in enumerate(filters):
        c = f.get("criteria", {})
        a = f.get("action", {})
        print(f"  [{i:2d}] id={f['id']}")
        print(f"        criteria: {c}")
        print(f"        action:   {a}")
    return filters


def backup_filters(service, output_path):
    result = service.users().settings().filters().list(userId="me").execute()
    filters = result.get("filter", [])
    Path(output_path).write_text(json.dumps(filters, indent=2))
    print(f"Backed up {len(filters)} filters to: {output_path}")
    return filters


def is_ghost_filter(f):
    """Return True if a filter has no meaningful routing action."""
    action = f.get("action", {})
    if not action:
        return True
    add = set(action.get("addLabelIds", []))
    remove = set(action.get("removeLabelIds", []))
    # Only system category labels — no user-created label routing
    if add and add.issubset(SYSTEM_CATEGORY_LABELS) and not remove:
        return True
    # Only inert actions (mark important, never spam, star) with no label routing
    all_action_keys = set(action.keys()) - {"addLabelIds", "removeLabelIds"}
    if not add and not remove and all_action_keys.issubset(INERT_ACTIONS_ONLY):
        return True
    return False


def audit_filters(service):
    result = service.users().settings().filters().list(userId="me").execute()
    filters = result.get("filter", [])
    ghosts = [f for f in filters if is_ghost_filter(f)]
    real = [f for f in filters if not is_ghost_filter(f)]

    print(f"\nTotal filters: {len(filters)}")
    print(f"Ghost filters (no meaningful action): {len(ghosts)}")
    print(f"Real filters: {len(real)}")

    if ghosts:
        print("\n--- Ghost filters ---")
        for f in ghosts:
            print(f"  {f['id']}  criteria={f.get('criteria', {})}  action={f.get('action', {})}")

    if real:
        print("\n--- Real filters ---")
        for f in real:
            print(f"  {f['id']}  criteria={f.get('criteria', {})}  action={f.get('action', {})}")

    return ghosts, real


def create_filter(service, from_senders, label_id, skip_inbox=False, mark_read=False):
    action = {"addLabelIds": [label_id]}
    remove = []
    if skip_inbox:
        remove.append("INBOX")
    if mark_read:
        remove.append("UNREAD")
    if remove:
        action["removeLabelIds"] = remove

    body = {
        "criteria": {"from": from_senders},  # space-separated; Gmail OR's them
        "action": action,
    }
    result = service.users().settings().filters().create(userId="me", body=body).execute()
    print(f"Filter created: {result['id']}")
    print(f"  From: {from_senders}")
    print(f"  Action: {action}")
    return result["id"]


def delete_filter(service, filter_id):
    service.users().settings().filters().delete(userId="me", id=filter_id).execute()
    print(f"Deleted filter: {filter_id}")


def delete_all_filters(service):
    """DESTRUCTIVE. Always backup first."""
    result = service.users().settings().filters().list(userId="me").execute()
    filters = result.get("filter", [])
    print(f"Deleting {len(filters)} filters...")
    for f in filters:
        service.users().settings().filters().delete(userId="me", id=f["id"]).execute()
        time.sleep(0.1)
    print("All filters deleted.")


def main():
    parser = argparse.ArgumentParser(description="Manage Gmail filters.")
    parser.add_argument("--token", required=True, help="Path to OAuth token JSON (needs gmail.settings.basic scope)")
    parser.add_argument("command", choices=["list", "backup", "audit", "create", "delete", "delete-all"])
    parser.add_argument("--output", default="filters_backup.json", help="Output path for backup")
    parser.add_argument("--from", dest="from_senders", help="Space-separated sender addresses/domains for filter")
    parser.add_argument("--label-id", help="Label ID to apply")
    parser.add_argument("--skip-inbox", action="store_true", help="Remove from inbox (skip inbox routing)")
    parser.add_argument("--mark-read", action="store_true", help="Mark as read on arrival (default: off)")
    parser.add_argument("--filter-id", help="Filter ID to delete")
    args = parser.parse_args()

    service = get_service(args.token)

    if args.command == "list":
        list_filters(service)
    elif args.command == "backup":
        backup_filters(service, args.output)
    elif args.command == "audit":
        audit_filters(service)
    elif args.command == "create":
        if not args.from_senders or not args.label_id:
            print("ERROR: --from and --label-id required for create")
            sys.exit(1)
        create_filter(service, args.from_senders, args.label_id,
                      skip_inbox=args.skip_inbox, mark_read=args.mark_read)
    elif args.command == "delete":
        if not args.filter_id:
            print("ERROR: --filter-id required for delete")
            sys.exit(1)
        delete_filter(service, args.filter_id)
    elif args.command == "delete-all":
        confirm = input("This will delete ALL filters. Type 'yes' to confirm: ")
        if confirm.strip().lower() == "yes":
            delete_all_filters(service)
        else:
            print("Aborted.")


if __name__ == "__main__":
    main()
