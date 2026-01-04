# Automatic-Clip-Exporter

A tiny Python script that **watches a folder for new `.mp4` files**, automatically **uploads them to PixelDrain**, and **copies the resulting share link to your clipboard**.

Made for quick esport / scrim / highlight clip sharing without manually uploading every time.

---

## What it does

- Polls a folder every few seconds
- Detects **new `.mp4` files** (ignores files that were already there when the script starts)
- Uploads via **PixelDrain API** using an HTTP `PUT`
- Prints the uploaded URL
- Copies the URL to your clipboard (`pyperclip`)
- Retries on common transient errors (429/5xx)

---

## Requirements

- Python 3.8+ recommended
- A PixelDrain API key

Python packages:
- `requests`
- `pyperclip`
- `urllib3` (installed as a dependency of `requests`)

Install dependencies:

```bash
pip install requests pyperclip
```

## Configure

Open auto_upload.py and set these values:

```py
WATCH_FOLDER = r"/path/to/your/folder"
PIXELDRAIN_API_KEY = "YOUR_API_KEY"
```

Notes:
- The folder must exist.
- The script will stop immediately if the API key is missing.

## Run

```bash
python AutomaticClipExporter.py
```

Keep it running. When a new .mp4 appears in the folder, you’ll see:
- Uploading: ...
- Uploaded: <https://pixeldrain.com/u/...>
- The link is copied to your clipboard.

Stop with Ctrl + C.

## How it works

- The script ignores files already present when it starts.
- It scans every POLL_INTERVAL seconds (default: 5).
- Only .mp4 files are uploaded.

## Disclaimer

Don’t commit your API key to a public repo.
