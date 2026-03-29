#!/usr/bin/env python3
"""
Build a sender index of the Gmail inbox.

Groups every inbox message by sender (email address), sorted by volume.
Produces sender_index.json — the foundation for the entire cleanup process.
Includes a next_sender_idx pointer so sessions can resume exactly where they left off.

Usage:
    python3 build_sender_index.py --token /path/to/token.json --output sender_index.json
"""
import argparse
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gmail_service import get_service


def get_all_inbox_ids(service):
    ids, pt = [], None
    while True:
        kw = {"userId": "me", "q": "in:inbox", "maxResults": 500}
        if pt:
            kw["pageToken"] = pt
        r = service.users().messages().list(**kw).execute()
        ids.extend(m["id"] for m in r.get("messages", []))
        pt = r.get("nextPageToken")
        print(f"\r  {len(ids)} message IDs collected...", end="", flush=True)
        if not pt:
            break
    print()
    return ids


def fetch_metadata_batch(service, ids):
    results = {}

    def cb(request_id, response, exception):
        if exception or not response:
            return
        hdrs = {h["name"].lower(): h["value"]
                for h in response.get("payload", {}).get("headers", [])}
        results[response["id"]] = {
            "from": hdrs.get("from", ""),
            "subject": hdrs.get("subject", "(no subject)"),
            "date": hdrs.get("date", ""),
            "ts": int(response.get("internalDate", "0")),
        }

    batch = service.new_batch_http_request(callback=cb)
    for mid in ids:
        batch.add(
            service.users().messages().get(
                userId="me", id=mid, format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            ),
            request_id=mid,
        )
    batch.execute()
    return results


def parse_sender(from_str):
    m = re.search(r"<([^>]+)>", from_str)
    if m:
        email = m.group(1).lower().strip()
        name = re.sub(r"\s*<[^>]+>", "", from_str).strip().strip("\"'")
        return name or email, email
    email = from_str.lower().strip()
    return email, email


def main():
    parser = argparse.ArgumentParser(description="Build Gmail sender index.")
    parser.add_argument("--token", required=True, help="Path to OAuth token JSON file")
    parser.add_argument("--output", default="sender_index.json", help="Output file path")
    args = parser.parse_args()

    service = get_service(args.token)
    print("=== Building Sender Index ===\n")

    print("Collecting inbox message IDs...")
    all_ids = get_all_inbox_ids(service)
    print(f"  {len(all_ids)} messages total\n")

    print("Fetching From/Subject/Date metadata (batch API)...")
    all_meta = {}
    n_batches = (len(all_ids) + 99) // 100
    for i in range(0, len(all_ids), 100):
        batch_num = i // 100 + 1
        print(f"\r  Batch {batch_num}/{n_batches}  ({len(all_meta)} done)", end="", flush=True)
        all_meta.update(fetch_metadata_batch(service, all_ids[i:i + 100]))
        if batch_num % 20 == 0:
            time.sleep(0.3)
    print(f"\n  {len(all_meta)} messages fetched\n")

    print("Grouping by sender...")
    groups = defaultdict(list)
    for mid, m in all_meta.items():
        name, email = parse_sender(m["from"])
        groups[email].append({
            "id": mid, "name": name,
            "subject": m["subject"], "date": m["date"], "ts": m["ts"],
        })

    for email in groups:
        groups[email].sort(key=lambda x: x["ts"], reverse=True)

    senders = sorted([
        {"email": email, "name": msgs[0]["name"], "count": len(msgs), "messages": msgs}
        for email, msgs in groups.items()
    ], key=lambda x: x["count"], reverse=True)

    index = {
        "built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_inbox_messages": len(all_meta),
        "total_senders": len(senders),
        "next_sender_idx": 0,
        "senders": senders,
    }

    Path(args.output).write_text(json.dumps(index, indent=2))
    print(f"Index saved to: {args.output}")
    print(f"\nTop 15 senders by volume:")
    for s in senders[:15]:
        print(f"  {s['count']:>5}  {s['email']}")
    print(f"\nTotal: {len(senders)} unique senders, {len(all_meta)} messages")


if __name__ == "__main__":
    main()
