"""
Create an Outlook draft via Microsoft Graph API.
Preserves HTML intact (no Word engine rewriting).
Uses MSAL token cache from the ms365 MCP server.
"""
import json
import sys
import msal
import requests

TOKEN_CACHE_PATH = "C:/Users/AdrianTurion/AppData/Local/npm-cache/_npx/813b81b976932cb5/node_modules/@softeria/ms-365-mcp-server/.token-cache.json"
CLIENT_ID = "084a3e9f-a9f4-43f7-89f9-d229cf97853e"
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["Mail.ReadWrite"]

def get_access_token():
    """Get access token from MSAL cache (shared with ms365 MCP)."""
    # Load the token cache from the MCP server
    cache = msal.SerializableTokenCache()
    with open(TOKEN_CACHE_PATH, "r") as f:
        cache_data = json.load(f)
    cache.deserialize(cache_data["data"])

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache,
    )

    accounts = app.get_accounts()
    if not accounts:
        print("ERROR: No accounts found in token cache. Run ms365 login first.")
        sys.exit(1)

    result = app.acquire_token_silent(SCOPES, account=accounts[0])
    if not result or "access_token" not in result:
        print("ERROR: Could not acquire token silently.", result)
        sys.exit(1)

    # Save back the cache in case tokens were refreshed
    if cache.has_state_changed:
        with open(TOKEN_CACHE_PATH, "w") as f:
            json.dump({
                "_cacheEnvelope": True,
                "data": cache.serialize(),
                "savedAt": int(__import__("time").time())
            }, f)

    return result["access_token"]


def create_draft(html_path, subject):
    """Create a draft message via Graph API with the HTML body intact."""
    token = get_access_token()

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    payload = {
        "subject": subject,
        "body": {
            "contentType": "HTML",
            "content": html_content,
        },
        "importance": "normal",
    }

    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )

    if resp.status_code == 201:
        msg = resp.json()
        print(f"Draft created successfully!")
        print(f"Subject: {msg['subject']}")
        print(f"Message ID: {msg['id']}")
        return msg
    else:
        print(f"ERROR {resp.status_code}: {resp.text}")
        sys.exit(1)


if __name__ == "__main__":
    html_file = sys.argv[1] if len(sys.argv) > 1 else "test-mjml-v4.html"
    subject = sys.argv[2] if len(sys.argv) > 2 else "[PREVIEW] Digest M&A - IT Services - Mars 2026"

    create_draft(html_file, subject)
