import cv2
import base64
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from logger import get_recent_events

_socketio = None

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "safevision-secret-key"
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",
        async_mode="threading",
        ping_timeout=10,
        ping_interval=5
    )

    global _socketio
    _socketio = socketio

    @app.route("/")
    def index():
        events = get_recent_events(50)
        return render_template("index.html", events=events)

    @app.route("/api/events")
    def api_events():
        rows = get_recent_events(100)
        return jsonify([
            {"ts": r[0], "event": r[1], "angle": r[2], "snapshot": r[3]}
            for r in rows
        ])

    @app.route("/api/status")
    def api_status():
        return jsonify({"status": "online"})

    return app, socketio

def push_frame(frame):
    if _socketio is None:
        return
    try:
        h, w = frame.shape[:2]
        if w > 640:
            frame = cv2.resize(frame, (640, int(h * 640 / w)))
        _, buf = cv2.imencode(
            ".jpg", frame,
            [cv2.IMWRITE_JPEG_QUALITY, 60]
        )
        b64 = base64.b64encode(buf).decode("utf-8")
        _socketio.emit("frame", {"img": b64})
    except Exception as e:
        print(f"[dashboard] push_frame error: {e}")

def push_event(data):
    if _socketio is None:
        return
    try:
        _socketio.emit("event", data)
    except Exception as e:
        print(f"[dashboard] push_event error: {e}")
