# Public Messenger

A very simple web-based messaging app built with Python's standard library.

Anyone with the link can open the page and send a message. Messages are stored in memory while the server is running.

## Run it

From this folder:

```bash
cd /Users/binosamuel/Projects/messenger
python3 app.py
```

Then open:

```text
http://localhost:8000
```

## Files

- `app.py` – starts the Python web server and handles chat requests
- `templates/index.html` – page layout
- `static/styles.css` – page styling
- `static/script.js` – browser logic for sending and loading messages

## Notes

- This is a simple local app meant for quick demo/testing use.
- It is not persistent across restarts because messages live in memory.
- If you want it accessible from other devices on the same network, open the machine's local IP instead of `localhost`.
# messenger
