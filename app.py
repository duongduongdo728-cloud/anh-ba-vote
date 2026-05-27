from flask import Flask, render_template, jsonify, request, session
from pathlib import Path
import sqlite3
import uuid
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "votes.db"

VALID_OPTIONS = {"option1", "option2"}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voter_id TEXT NOT NULL UNIQUE,
                option TEXT NOT NULL CHECK(option IN ('option1', 'option2')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


@app.before_request
def ensure_voter_id():
    if "voter_id" not in session:
        session["voter_id"] = str(uuid.uuid4())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/results")
def results():
    init_db()

    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT option, COUNT(*) AS count
            FROM votes
            GROUP BY option
            """
        ).fetchall()

    counts = {
        "option1": 0,
        "option2": 0,
    }

    for row in rows:
        counts[row["option"]] = row["count"]

    total = counts["option1"] + counts["option2"]

    voted_option = None
    with get_db() as conn:
        current_vote = conn.execute(
            "SELECT option FROM votes WHERE voter_id = ?",
            (session["voter_id"],),
        ).fetchone()

    if current_vote:
        voted_option = current_vote["option"]

    return jsonify({
        "counts": counts,
        "total": total,
        "voted_option": voted_option,
    })


@app.route("/api/vote", methods=["POST"])
def vote():
    init_db()

    payload = request.get_json(silent=True) or {}
    option = payload.get("option")

    if option not in VALID_OPTIONS:
        return jsonify({"ok": False, "message": "Lựa chọn không hợp lệ."}), 400

    voter_id = session["voter_id"]

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO votes (voter_id, option) VALUES (?, ?)",
                (voter_id, option),
            )
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({
            "ok": False,
            "message": "Bạn đã vote trên trình duyệt này rồi."
        }), 409

    return jsonify({"ok": True, "message": "Cảm ơn bạn đã vote!"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
