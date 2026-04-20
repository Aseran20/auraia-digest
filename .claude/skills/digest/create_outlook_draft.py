"""
Create an Outlook draft via win32com (Outlook desktop COM automation).

Usage:
    python create_outlook_draft.py <html_path> [subject]

If subject is omitted, derives one from the filename.
"""
import sys
import os
import re
import win32com.client


def derive_subject(html_path: str) -> str:
    base = os.path.splitext(os.path.basename(html_path))[0]
    m = re.match(r"(\d{4}-\d{2}-\d{2})_digest_(.+)", base)
    if not m:
        return f"Digest M&A — {base}"
    date, topic = m.group(1), m.group(2).replace("_", " ").replace("-", " ")
    return f"Digest M&A — {topic} — {date}"


def create_draft(html_path: str, subject: str) -> None:
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.HTMLBody = html
    mail.Display(False)
    print(f"Draft opened: {subject}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_outlook_draft.py <html_path> [subject]")
        sys.exit(1)
    html_path = sys.argv[1]
    subject = sys.argv[2] if len(sys.argv) > 2 else derive_subject(html_path)
    create_draft(html_path, subject)
