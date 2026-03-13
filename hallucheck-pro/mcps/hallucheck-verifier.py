#!/usr/bin/env python3
"""
Hallucheck Verifier MCP Server

Verifies academic references via CrossRef, OpenLibrary, and Google Books APIs.
Implements the Model Context Protocol (MCP) over stdio.

ISBN resolution strategy (fallback chain):
  1. OpenLibrary  (openlibrary.org)  — primary; returns rich metadata
  2. Google Books (googleapis.com)   — fallback if OpenLibrary is blocked/unavailable

Tools:
- verify_reference: Verify a single reference (DOI, ISBN, or URL)
"""

import json
import sys
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List
import re


def fetch_crossref(doi: str) -> Optional[Dict[str, Any]]:
    """Fetch metadata from CrossRef API for a DOI."""
    try:
        url = f"https://api.crossref.org/works/{doi}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "ok" and data.get("message"):
                msg = data["message"]
                return {
                    "success": True,
                    "source": "CrossRef",
                    "title": msg.get("title", [None])[0] if msg.get("title") else None,
                    "authors": [f"{a.get('family', '')} {a.get('given', '')}".strip() for a in msg.get("author", [])],
                    "year": msg.get("published", {}).get("date-parts", [[None]])[0][0],
                    "journal": msg.get("container-title", [None])[0] if msg.get("container-title") else None,
                    "volume": msg.get("volume"),
                    "issue": msg.get("issue"),
                    "pages": msg.get("page"),
                    "doi": msg.get("DOI")
                }
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, Exception) as e:
        return {"success": False, "source": "CrossRef", "error": str(e)}
    return None


def fetch_openlibrary(isbn: str) -> Optional[Dict[str, Any]]:
    """Fetch metadata from OpenLibrary API for an ISBN."""
    try:
        isbn_clean = isbn.replace("-", "")
        url = f"https://openlibrary.org/isbn/{isbn_clean}.json"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return {
                "success": True,
                "source": "OpenLibrary",
                "title": data.get("title"),
                "authors": [a.get("name", "") for a in data.get("authors", [])],
                "publishers": data.get("publishers", []),
                "publish_date": data.get("publish_date"),
                "isbn": isbn_clean
            }
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, Exception) as e:
        return {"success": False, "source": "OpenLibrary", "error": str(e)}
    return None


def fetch_google_books(isbn: str) -> Optional[Dict[str, Any]]:
    """Fetch metadata from Google Books API for an ISBN (fallback for OpenLibrary)."""
    try:
        isbn_clean = isbn.replace("-", "")
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_clean}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get("totalItems", 0) == 0 or not data.get("items"):
                return {"success": False, "source": "GoogleBooks", "error": "No results found"}
            info = data["items"][0].get("volumeInfo", {})
            # Normalize publishedDate to year only
            raw_date = info.get("publishedDate", "")
            year = raw_date[:4] if raw_date else None
            return {
                "success": True,
                "source": "GoogleBooks",
                "title": info.get("title"),
                "authors": info.get("authors", []),
                "publishers": [info.get("publisher")] if info.get("publisher") else [],
                "publish_date": raw_date,
                "year": year,
                "isbn": isbn_clean
            }
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, Exception) as e:
        return {"success": False, "source": "GoogleBooks", "error": str(e)}
    return None


def fetch_isbn(isbn: str) -> Dict[str, Any]:
    """
    Resolve an ISBN using the fallback chain:
      1. OpenLibrary (primary)
      2. Google Books (fallback)
    Returns the first successful result, or a combined error dict if both fail.
    """
    result = fetch_openlibrary(isbn)
    if result and result.get("success"):
        return result

    ol_error = result.get("error", "unknown") if result else "no response"

    # OpenLibrary failed — try Google Books
    gb_result = fetch_google_books(isbn)
    if gb_result and gb_result.get("success"):
        gb_result["fallback"] = True
        gb_result["openlibrary_error"] = ol_error
        return gb_result

    # Both failed
    return {
        "success": False,
        "source": "OpenLibrary+GoogleBooks",
        "fallback_attempted": True,
        "openlibrary_error": ol_error,
        "google_books_error": gb_result.get("error", "unknown") if gb_result else "no response",
        "error": f"Both OpenLibrary and Google Books unavailable. OL: {ol_error}"
    }


def fetch_url(url: str) -> Optional[Dict[str, Any]]:
    """Fetch a bare URL and check if it's accessible."""
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            content = response.read().decode(errors='ignore')
            return {
                "success": True,
                "url": url,
                "status_code": response.status,
                "content_length": len(content),
                "accessible": True
            }
    except (urllib.error.HTTPError, urllib.error.URLError, Exception) as e:
        return {"success": False, "url": url, "error": str(e), "accessible": False}


def identify_reference_type(ref_id: str) -> tuple[str, str]:
    """Identify the type of reference and normalize it."""
    if ref_id.startswith("10.") or "doi:" in ref_id.lower():
        doi = ref_id.replace("doi:", "").replace("DOI:", "").strip()
        return "doi", doi

    if ref_id.startswith("978") or ref_id.startswith("979"):
        return "isbn", ref_id

    if ref_id.startswith("http://") or ref_id.startswith("https://"):
        return "url", ref_id

    return "unknown", ref_id


def verify_reference(ref_id: str, expected_data: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Verify a single reference.

    Args:
        ref_id: DOI, ISBN, or URL to verify
        expected_data: Optional dict with expected metadata (title, authors, year, journal, volume, issue, pages)

    Returns:
        Dict with verification results including success, source, metadata, and mismatches.
        For ISBNs, 'source' will be 'OpenLibrary' (primary) or 'GoogleBooks' (fallback),
        and 'fallback': True will be set if Google Books was used.
    """
    ref_type, identifier = identify_reference_type(ref_id)

    if ref_type == "doi":
        result = fetch_crossref(identifier)
    elif ref_type == "isbn":
        result = fetch_isbn(identifier)   # OpenLibrary → Google Books fallback chain
    elif ref_type == "url":
        result = fetch_url(identifier)
    else:
        result = {"success": False, "error": "Unknown reference type"}

    if not result:
        result = {"success": False, "error": "No data returned"}

    # Compare with expected data if provided
    mismatches = []
    if expected_data and result.get("success"):
        if "title" in expected_data and expected_data["title"]:
            if result.get("title", "").lower() != expected_data["title"].lower():
                mismatches.append({
                    "field": "title",
                    "expected": expected_data["title"],
                    "returned": result.get("title")
                })

        if "year" in expected_data and expected_data["year"]:
            if str(result.get("year")) != str(expected_data["year"]):
                mismatches.append({
                    "field": "year",
                    "expected": expected_data["year"],
                    "returned": result.get("year")
                })

        if "authors" in expected_data and expected_data["authors"]:
            expected_authors = set(expected_data["authors"].lower().split(";"))
            returned_authors = set(" ".join(result.get("authors", [])).lower().split(";"))
            if not expected_authors.issubset(returned_authors):
                mismatches.append({
                    "field": "authors",
                    "expected": expected_data["authors"],
                    "returned": "; ".join(result.get("authors", []))
                })

    result["mismatches"] = mismatches
    result["reference_type"] = ref_type
    return result


def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle an MCP request."""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

    try:
        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "verify_reference",
                            "description": (
                                "Verify an academic reference via CrossRef (DOI), "
                                "OpenLibrary with Google Books fallback (ISBN), or bare URL check. "
                                "ISBNs are tried against OpenLibrary first; if blocked or unavailable, "
                                "Google Books is used automatically as fallback."
                            ),
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "reference_id": {
                                        "type": "string",
                                        "description": "DOI (10.xxx/...), ISBN (978...), or URL (https://...)"
                                    },
                                    "expected_title": {
                                        "type": "string",
                                        "description": "Expected article/book title (optional, for comparison)"
                                    },
                                    "expected_year": {
                                        "type": "integer",
                                        "description": "Expected publication year (optional)"
                                    },
                                    "expected_authors": {
                                        "type": "string",
                                        "description": "Expected authors semicolon-separated (optional)"
                                    }
                                },
                                "required": ["reference_id"]
                            }
                        }
                    ]
                }
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_input = params.get("arguments", {})

            if tool_name == "verify_reference":
                ref_id = tool_input.get("reference_id")
                expected = {}
                if tool_input.get("expected_title"):
                    expected["title"] = tool_input["expected_title"]
                if tool_input.get("expected_year"):
                    expected["year"] = tool_input["expected_year"]
                if tool_input.get("expected_authors"):
                    expected["authors"] = tool_input["expected_authors"]

                result = verify_reference(ref_id, expected if expected else None)

                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "type": "tool_result",
                        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                    }
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }


def main():
    """Main MCP server loop."""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line)
            response = handle_request(request)

            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

        except json.JSONDecodeError:
            continue
        except KeyboardInterrupt:
            break
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(error_response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
