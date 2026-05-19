import cv2
import threading
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")

        self.frame   = None
        self.lock    = threading.Lock()
        self.running = True

        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()
        print("[camera] Threaded camera started")

    def _reader(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame

    def read(self):
        with self.lock:
            if self.frame is None:
                return None
            return self.frame.copy()

    def release(self):
        self.running = False
        self.thread.join(timeout=2)
        self.cap.release()
        print("[camera] Camera released")
