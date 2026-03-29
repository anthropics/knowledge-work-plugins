#!/usr/bin/env python3
"""
Shared Gmail service builder. Import this in other scripts.

Usage:
    from gmail_service import get_service
    service = get_service("/path/to/token.json")
"""
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def get_service(token_path: str):
    """Build and return an authenticated Gmail API service object.
    Automatically refreshes the token if expired."""
    with open(token_path) as f:
        data = json.load(f)

    creds = Credentials(
        token=data.get("token") or data.get("access_token"),
        refresh_token=data.get("refresh_token"),
        token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        scopes=data.get("scopes"),
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        data["token"] = creds.token
        with open(token_path, "w") as f:
            json.dump(data, f, indent=2)

    return build("gmail", "v1", credentials=creds)
