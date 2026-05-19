import cv2

SKELETON = [
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (5, 11), (6, 12), (11, 12),
    (11, 13), (13, 15), (12, 14), (14, 16)
]

COLORS = {
    "normal":        (0, 200, 100),
    "fall_detected": (0, 60, 255),
    "fall_ongoing":  (0, 120, 255),
    "unknown":       (150, 150, 150),
}

def draw_overlay(frame, persons, status, fps):
    out   = frame.copy()
    color = COLORS.get(status, (150, 150, 150))

    for person in persons:
        kps = person["keypoints"].astype(int)
        for a, b in SKELETON:
            if kps[a][0] > 0 and kps[b][0] > 0:
                cv2.line(out, tuple(kps[a]), tuple(kps[b]), color, 2)
        for k in kps:
            if k[0] > 0:
                cv2.circle(out, tuple(k), 4, color, -1)
        if person["torso_angle"] is not None:
            cv2.putText(
                out,
                f"{person['torso_angle']:.1f}deg",
                (int(kps[5][0]), int(kps[5][1]) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1
            )

    label    = "FALL DETECTED!" if "fall" in status else "Normal"
    bg_color = (0, 0, 180) if "fall" in status else (20, 20, 20)
    cv2.rectangle(out, (10, 10), (300, 50), bg_color, -1)
    cv2.putText(out, label, (18, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(out, f"FPS: {fps:.1f}", (540, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    return out

