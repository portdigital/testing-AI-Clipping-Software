"""
YOLO Face Tracking + Auto Reframe 9:16 untuk YouTube Shorts.
Menggunakan Ultralytics YOLO dengan fallback ke OpenCV Haar Cascade.
"""
import cv2
import numpy as np

from config_ican import YOLO_MODEL


class YOLOFaceTracker:
    """Deteksi wajah/orang dengan YOLO dan crop ke format 9:16."""

    def __init__(self, model_path=None):
        self.model_path = model_path or YOLO_MODEL
        self._model = None
        self.face_cache = {}
        self._use_yolo = False
        self._face_cascade = None
        self._init_detector()

    def _init_detector(self):
        try:
            from ultralytics import YOLO
            print(f"🎯 Loading YOLO model: {self.model_path}")
            self._model = YOLO(self.model_path)
            self._use_yolo = True
            print("✅ YOLO face/person tracker siap")
        except Exception as e:
            print(f"⚠️  YOLO tidak tersedia ({e}), fallback ke OpenCV Haar Cascade")
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self._face_cascade = cv2.CascadeClassifier(cascade_path)

    def _detect_yolo(self, frame):
        """Deteksi person (class 0) atau face dengan YOLO."""
        h, w, _ = frame.shape
        results = self._model(frame, verbose=False, conf=0.35)

        detections = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                # class 0 = person di COCO dataset
                if cls_id not in (0,):
                    continue
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)
                area = (x2 - x1) * (y2 - y1)
                detections.append({
                    'center_x': cx,
                    'center_y': cy,
                    'width': int(x2 - x1),
                    'height': int(y2 - y1),
                    'confidence': conf,
                    'area': area,
                })

        return sorted(detections, key=lambda d: d['confidence'] * d['area'], reverse=True)

    def _detect_haar(self, frame):
        """Fallback deteksi wajah dengan Haar Cascade."""
        h, w, _ = frame.shape
        scale = 0.5
        small = cv2.resize(frame, (int(w * scale), int(h * scale)))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        faces = self._face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

        detections = []
        for (x, y, fw, fh) in faces:
            x, y, fw, fh = int(x / scale), int(y / scale), int(fw / scale), int(fh / scale)
            detections.append({
                'center_x': x + fw // 2,
                'center_y': y + fh // 2,
                'width': fw,
                'height': fh,
                'confidence': 0.8,
                'area': fw * fh,
            })
        return sorted(detections, key=lambda d: d['area'], reverse=True)

    def detect_in_frame(self, frame, frame_time=None):
        if frame_time is not None and frame_time in self.face_cache:
            return self.face_cache[frame_time]

        try:
            if self._use_yolo:
                result = self._detect_yolo(frame)
            else:
                result = self._detect_haar(frame)
        except Exception:
            result = []

        if frame_time is not None:
            self.face_cache[frame_time] = result
        return result

    def smooth_trajectory(self, positions, window_size=5):
        if len(positions) <= window_size:
            return positions
        smoothed = []
        for i in range(len(positions)):
            start = max(0, i - window_size // 2)
            end = min(len(positions), i + window_size // 2 + 1)
            window = positions[start:end]
            smoothed.append((
                sum(p[0] for p in window) / len(window),
                sum(p[1] for p in window) / len(window),
            ))
        return smoothed

    def track_and_reframe(self, clip):
        """
        Track subjek utama dan reframe ke 9:16 (1080x1920 target).
        Returns cropped clip dalam aspect ratio 9:16.
        """
        width, height = clip.size
        target_width = int(height * 9 / 16)
        if target_width % 2 != 0:
            target_width -= 1

        if width <= target_width:
            print("    ⏩ Video sudah 9:16")
            return clip

        print("    🎯 YOLO tracking + auto reframe 9:16...")
        self.face_cache = {}

        positions = []
        num_samples = min(10, max(4, int(clip.duration / 2)))
        sample_times = np.linspace(0, max(0.01, clip.duration - 0.01), num_samples)

        for i, t in enumerate(sample_times):
            frame = clip.get_frame(t)
            detections = self.detect_in_frame(frame, frame_time=t)
            if detections:
                positions.append(detections[0]['center_x'])
            elif positions:
                positions.append(positions[-1])
            else:
                positions.append(width // 2)

        if positions:
            smoothed = self.smooth_trajectory([(p, height // 2) for p in positions])
            center_x = int(np.median([p[0] for p in smoothed]))
        else:
            center_x = width // 2

        center_x = max(target_width // 2, min(width - target_width // 2, center_x))
        left = center_x - target_width // 2

        self.face_cache = {}
        cropped = clip.crop(x1=left, width=target_width)
        print(f"    ✅ Reframed: {target_width}x{height} (9:16)")
        return cropped

    def close(self):
        self.face_cache = {}
