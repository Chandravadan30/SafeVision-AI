import cv2
import time
import threading
from camera import Camera
from pose_estimator import PoseEstimator
from fall_detector import FallDetector
from alerts import trigger_alert
from display import draw_overlay
from logger import init_db
from config import HEADLESS, INFERENCE_EVERY_N
from dashboard.app import create_app, push_frame, push_event

def main():
    init_db()

    print("[main] Initializing camera...")
    cam = Camera()

    print("[main] Loading pose model...")
    pose = PoseEstimator()

    detect = FallDetector()

    print("[main] Starting dashboard server on port 5000...")
    app, socketio = create_app()
    t = threading.Thread(
        target=lambda: socketio.run(app, host="0.0.0.0", port=5000, use_reloader=False)
    )
    t.daemon = True
    t.start()

    prev_time     = time.time()
    alerted       = False
    frame_count   = 0
    persons       = []
    status        = "normal"
    fps           = 0.0
    last_push     = time.time()
    PUSH_INTERVAL = 1.0 / 15

    print("[main] Pipeline running. Open http://10.0.0.63:5000 in your browser.")
    print("[main] Press Ctrl+C to stop.")

    try:
        while True:
            frame = cam.read()
            if frame is None:
                time.sleep(0.005)
                continue

            frame_count += 1

            if frame_count % INFERENCE_EVERY_N == 0:
                persons = pose.estimate(frame)
                angle   = persons[0]["torso_angle"] if persons else None
                status  = detect.update(angle)

                if status == "fall_detected" and not alerted:
                    print(f"[main] FALL DETECTED — angle: {angle:.1f}deg")
                    trigger_alert(frame, angle)
                    push_event({"status": "fall_detected", "angle": round(angle, 1)})
                    alerted = True
                elif status == "fall_ongoing" and alerted:
                    push_event({
                        "status": "fall_ongoing",
                        "angle": round(angle, 1) if angle else None
                    })
                elif status == "normal":
                    if alerted:
                        push_event({"status": "normal"})
                    alerted = False

            now       = time.time()
            fps       = 1.0 / (now - prev_time + 1e-6)
            prev_time = now

            out = draw_overlay(frame, persons, status, fps)

            if now - last_push >= PUSH_INTERVAL:
                push_frame(out)
                last_push = now

            if not HEADLESS:
                cv2.imshow("SafeVision", out)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    except KeyboardInterrupt:
        print("\n[main] Shutting down...")
    finally:
        cam.release()
        if not HEADLESS:
            cv2.destroyAllWindows()
        print("[main] Done.")

if __name__ == "__main__":
    main()
