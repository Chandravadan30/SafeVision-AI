from collections import deque
from config import FALL_ANGLE_THRESH, FALL_FRAME_WINDOW

class FallDetector:
    def __init__(self):
        self.angle_history = deque(maxlen=FALL_FRAME_WINDOW)
        self.fall_active   = False

    def update(self, torso_angle, hip_y=None):
        if torso_angle is None:
            self.angle_history.append(False)
            return "unknown"

        exceeded = torso_angle > FALL_ANGLE_THRESH
        self.angle_history.append(exceeded)

        print(f"[detector] angle={torso_angle:.1f}  exceeded={exceeded}  "
              f"history={sum(self.angle_history)}/{len(self.angle_history)}  "
              f"fall_active={self.fall_active}")

        votes = sum(self.angle_history)

        if votes >= 3 and not self.fall_active:
            self.fall_active = True
            print(f"[detector] *** FALL CONFIRMED *** angle={torso_angle:.1f}")
            return "fall_detected"
        elif votes >= 3 and self.fall_active:
            return "fall_ongoing"
        elif votes == 0:
            self.fall_active = False
            return "normal"

        return "normal"
