import cv2
import numpy as np
import torch
from ultralytics import YOLO
from config import MODEL_PATH, CONF_THRESHOLD

SHOULDER_L, SHOULDER_R = 5, 6
HIP_L, HIP_R           = 11, 12

class PoseEstimator:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else "cpu"
        print(f"[pose] Using device: {'GPU (CUDA)' if self.device == 0 else 'CPU — GPU not found, will be slow'}")
        self.model = YOLO(MODEL_PATH)
        if self.device == 0:
            try:
                dummy = torch.zeros(1, 3, 320, 320).cuda()
                self.model(dummy, verbose=False, device=self.device)
                print("[pose] GPU warmup done")
            except Exception as e:
                print(f"[pose] GPU warmup skipped: {e}")

    def estimate(self, frame):
        small = cv2.resize(frame, (320, 320))
        results = self.model(
            small,
            conf=CONF_THRESHOLD,
            verbose=False,
            device=self.device,
            imgsz=320
        )

        h_orig, w_orig = frame.shape[:2]
        scale_x = w_orig / 320
        scale_y = h_orig / 320

        persons = []
        for r in results:
            if r.keypoints is None:
                continue
            kps_list = r.keypoints.xy.cpu().numpy()
            boxes    = r.boxes.xyxy.cpu().numpy() if r.boxes else None
            for i, kps in enumerate(kps_list):
                scaled_kps = kps.copy()
                scaled_kps[:, 0] *= scale_x
                scaled_kps[:, 1] *= scale_y
                torso_angle = self._torso_angle(scaled_kps)
                persons.append({
                    "keypoints":   scaled_kps,
                    "torso_angle": torso_angle,
                    "bbox":        boxes[i] if boxes is not None and i < len(boxes) else None,
                })
        return persons

    def _torso_angle(self, kps):
        sl = kps[SHOULDER_L]
        sr = kps[SHOULDER_R]
        hl = kps[HIP_L]
        hr = kps[HIP_R]

        shoulder_mid = None
        hip_mid      = None

        if sl[0] > 0 and sl[1] > 0 and sr[0] > 0 and sr[1] > 0:
            shoulder_mid = (sl + sr) / 2
        elif sl[0] > 0 and sl[1] > 0:
            shoulder_mid = sl
        elif sr[0] > 0 and sr[1] > 0:
            shoulder_mid = sr

        if hl[0] > 0 and hl[1] > 0 and hr[0] > 0 and hr[1] > 0:
            hip_mid = (hl + hr) / 2
        elif hl[0] > 0 and hl[1] > 0:
            hip_mid = hl
        elif hr[0] > 0 and hr[1] > 0:
            hip_mid = hr

        if shoulder_mid is None or hip_mid is None:
            return None

        torso_vec = shoulder_mid - hip_mid
        angle_from_vertical = np.degrees(
            np.arctan2(abs(torso_vec[0]), abs(torso_vec[1]) + 1e-6)
        )
        return angle_from_vertical
