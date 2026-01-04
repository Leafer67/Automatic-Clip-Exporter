
# auto_upload.py
import os
import time
import json
import subprocess
import mimetypes
from urllib.parse import quote

import requests
import pyperclip
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ---- CONFIG ----
WATCH_FOLDER = r"/path/to/your/clips"
PIXELDRAIN_API_KEY = "YOUR_KEY_HERE"

POLL_INTERVAL = 5  # seconds
# ----------------

if not PIXELDRAIN_API_KEY:
    raise SystemExit("Put PIXELDRAIN_API_KEY into the script.")

# mark existing files as processed so they're ignored on startup
processed = set(os.listdir(WATCH_FOLDER))

session = requests.Session()
session.headers.update({"User-Agent": "MR-AutoClipUploader/1.0"})
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=frozenset(["PUT", "POST", "GET"])
)
session.mount("https://", HTTPAdapter(max_retries=retries))


def upload_put(path, filename):
    # ensure name length <= 255 (server limit)
    name = filename
    if len(name) > 250:
        name = name[:250]
    encoded_name = quote(name, safe="")
    url = f"https://pixeldrain.com/api/file/{encoded_name}"

    size = os.path.getsize(path)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    headers = {
        "Content-Type": mime,
        "Content-Length": str(size)
    }
    auth = ("", PIXELDRAIN_API_KEY)  # username can be empty, key in password field

    try:
        with open(path, "rb") as f:
            # data=f will stream the file body
            resp = session.put(url, data=f, headers=headers, auth=auth, timeout=(10, 600))
        if resp.status_code in (200, 201):
            data = resp.json()
            return f"<https://pixeldrain.com/u/{data['id']}>"
        else:
            # try decode JSON error if present
            try:
                err = resp.json()
            except Exception:
                err = resp.text
            print("PUT returned", resp.status_code, err)
            return None
    except requests.RequestException as e:
        print("requests exception during PUT:", repr(e))
        return None


if __name__ == "__main__":
    try:
        print("Ready to upload new files")
        while True:
            for fname in os.listdir(WATCH_FOLDER):
                if not fname.lower().endswith(".mp4"):
                    continue
                if fname in processed:
                    continue

                path = os.path.join(WATCH_FOLDER, fname)
                print("Uploading:", fname)

                url = upload_put(path, fname)

                if url:
                    print("Uploaded:", url)
                    pyperclip.copy(url)
                    print("Link copied to clipboard.")
                    processed.add(fname)
                else:
                    print("Upload failed for", fname, "- will retry later")
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped by user.")
