from flask import Flask, request, jsonify, redirect, abort
from .models import URLStore
from .utils import is_valid_url

app = Flask(__name__)
store = URLStore()

# 1. Basic health check
@app.route("/")
def health_check():
    return jsonify({"status": "healthy", "service": "URL Shortener API"})

# 2. API health check
@app.route("/api/health")
def api_health():
    return jsonify({"status": "ok", "message": "URL Shortener API is running"})

# 3. Shorten URL
@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json(silent=True)
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    long_url = data["url"]
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    code = store.create(long_url)
    # build the short URL dynamically
    short_url = request.host_url.rstrip("/") + "/" + code
    return jsonify({"short_code": code, "short_url": short_url}), 201

# 4. Redirect endpoint
@app.route("/<code>")
def redirect_to_long(code):
    entry = store.get(code)
    if not entry:
        abort(404)
    store.increment(code)
    return redirect(entry["url"])

# 5. Analytics endpoint
@app.route("/api/stats/<code>")
def stats(code):
    entry = store.get(code)
    if not entry:
        abort(404)
    return jsonify({
        "url": entry["url"],
        "clicks": entry["clicks"],
        "created_at": entry["created_at"]
    })

# JSON 404 handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    # for local development only
    app.run(host="0.0.0.0", port=5000, debug=True)
