#!/usr/bin/env python3
"""
Fetch a Jira issue and save it as markdown.

A description containing the producer's overflow marker authorizes the newest
exact ``<issue-key>-strategy.md`` attachment; matching attachments without that
marker are orphaned and ignored.

Usage:
    python fetch_issue.py <ISSUE_KEY> [--output <FILE>]

Environment variables:
- JIRA_URL: Base URL for the Jira instance (required)
- JIRA_USER: Username or email for authentication (required)
- JIRA_TOKEN: API token for authentication (required)

Examples:
    python fetch_issue.py RHAISTRAT-400
    python fetch_issue.py RHOAIENG-48676 --output strategy.md
"""

import argparse
import sys

import requests

from scripts.jira_utils import AttachmentFetchError, get_issue
from scripts.strategy_source import format_issue_as_markdown
from scripts.utils.error_utils import exit_error


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Fetch a Jira issue and save it as markdown")
    parser.add_argument("issue_key", help="The Jira issue key (e.g., RHAISTRAT-400)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        # Fetch the issue
        issue_data = get_issue(args.issue_key, fields=None)

        # Format as markdown
        markdown = format_issue_as_markdown(issue_data)

        # Write to file or stdout
        if args.output:
            with open(args.output, "w") as f:
                f.write(markdown)
            print(f"Issue {args.issue_key} saved to {args.output}", file=sys.stderr)
        else:
            print(markdown)

    except (requests.RequestException, AttachmentFetchError):
        # Request exceptions can contain URLs, query parameters, or server response bodies.
        # Keep the direct CLI useful without exposing those details; resolve_strategy.py
        # invokes the formatter directly and retains the typed exception for its stable mapping.
        exit_error("Error: Jira issue fetch failed")


if __name__ == "__main__":
    main()
