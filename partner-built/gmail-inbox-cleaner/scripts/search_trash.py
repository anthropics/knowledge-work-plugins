#!/usr/bin/env python3
"""
Search trash accurately using the Gmail API.

NOTE: The Gmail MCP connector does not reliably isolate trash — it returns
inbox/sent/draft messages regardless of 'in:trash' in the query. This script
uses the API directly with labelIds=['TRASH'] for accurate results.

Outputs a JSON file with matching message metadata for review.

Usage:
    python3 search_trash.py --token token.json --query "invoice OR receipt OR contract" --output trash_hits.json
    python3 search_trash.py --token token.json --output trash_hits.json  # all trash messages
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gmail_service import get_service


def search_trash(service, query_fragment=""):
    q = f"in:trash {query_fragment}".strip()
    ids, pt = [], None
    while True:
        kw = {"userId": "me", "q": q, "labelIds": ["TRASH"], "maxResults": 500}
        if pt:
            kw["pageToken"] = pt
        r = service.users().messages().list(**kw).execute()
        ids.extend(m["id"] for m in r.get("messages", []))
        pt = r.get("nextPageToken")
        print(f"\r  {len(ids)} matching messages...", end="", flush=True)
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


def main():
    parser = argparse.ArgumentParser(description="Search Gmail trash accurately.")
    parser.add_argument("--token", required=True, help="Path to OAuth token JSON")
    parser.add_argument("--query", default="", help="Search query fragment (appended to 'in:trash')")
    parser.add_argument("--output", default="trash_hits.json", help="Output JSON file path")
    args = parser.parse_args()

    service = get_service(args.token)
    print(f"Searching trash: '{('in:trash ' + args.query).strip()}'")

    ids = search_trash(service, args.query)
    print(f"Found {len(ids)} messages. Fetching metadata...")

    all_meta = {}
    for i in range(0, len(ids), 100):
        all_meta.update(fetch_metadata_batch(service, ids[i:i + 100]))
        if i % 2000 == 0 and i > 0:
            time.sleep(0.3)

    # Group by sender
    from collections import defaultdict
    import re
    groups = defaultdict(list)
    for mid, m in all_meta.items():
        from_str = m["from"]
        match = re.search(r"<([^>]+)>", from_str)
        email = match.group(1).lower() if match else from_str.lower()
        groups[email].append({"id": mid, "subject": m["subject"], "date": m["date"]})

    results = sorted([
        {"email": email, "count": len(msgs), "messages": msgs}
        for email, msgs in groups.items()
    ], key=lambda x: x["count"], reverse=True)

    output = {"query": args.query, "total_hits": len(ids), "senders": results}
    Path(args.output).write_text(json.dumps(output, indent=2))

    print(f"\nTop senders in results:")
    for s in results[:20]:
        print(f"  {s['count']:>5}  {s['email']}")
    print(f"\nFull results saved to: {args.output}")


if __name__ == "__main__":
    main()
