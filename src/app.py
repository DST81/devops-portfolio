from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/ready")
def ready():
    return jsonify(status="ready")

@app.get("/api/books")
def get_books():
    return jsonify(books=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)