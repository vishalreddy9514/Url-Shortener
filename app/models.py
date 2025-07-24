
import threading
from datetime import datetime, timezone
from .utils import generate_short_code

class URLStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {}  # code → {url, clicks, created_at}

    def create(self, url: str) -> str:
        """Generate a unique code, store the URL, timestamp & zero clicks."""
        with self._lock:
            # loop until we find an unused code
            while True:
                code = generate_short_code()
                if code not in self._data:
                    self._data[code] = {
                        "url": url,
                        "clicks": 0,
                        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

                    }
                    return code

    def get(self, code: str) -> dict | None:
        """Return the entry or None if missing."""
        with self._lock:
            return self._data.get(code)

    def increment(self, code: str) -> None:
        """Increment click count (assumes code exists)."""
        with self._lock:
            self._data[code]["clicks"] += 1
