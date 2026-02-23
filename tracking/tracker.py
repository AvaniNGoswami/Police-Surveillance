import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

class PersonTracker():
    def __init__(self):
        self.model = YOLO("yolov8s.pt")
        self.tracker = DeepSort(max_age=30,n_init=3)
        self.class_names = self.model.model.names

    def process_frame(self,frame):
        results = self.model(frame, classes=[0,24,26,28,39,43,67])[0]
        detections = []

        for box in results.boxes:
            x1,y1,x2,y2 = box.xyxy[0]
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            label = self.class_names[cls_id]
            detections.append((
                [int(x1), int(y1), int(x2 - x1), int(y2 - y1)],
                conf,
                label
            ))

        tracks = self.tracker.update_tracks(detections,frame=frame)

        person_track = []

        for track in tracks:
            if not track.is_confirmed():
                continue

            l,t,r,b = track.to_ltrb()
            track_id = track.track_id
            person_track.append({
                "id":track_id,
                "bbox":[int(l),int(t),int(r),int(b)],
                'label':track.get_det_class()
            })

        return person_track

            
