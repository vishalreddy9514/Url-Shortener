import string, secrets
from urllib.parse import urlparse

ALPHABET = string.ascii_letters + string.digits

def generate_short_code(length: int = 6) -> str:
    """Return a cryptographically secure random alphanumeric string."""
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

def is_valid_url(url: str) -> bool:
    """
    Very basic check: must parse, have http(s) scheme and a netloc.
    """
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https") and bool(result.netloc)
    except Exception:
        return False
