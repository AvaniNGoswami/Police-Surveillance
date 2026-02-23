# import cv2
# import supervision as sv
# from ultralytics import YOLO
# from tracking.tracker import PersonTracker
# from tracking.track_state import TrackStateManager

# model = YOLO("yolov8s.pt")
# # model = YOLO("yolov8n.pt")

# video_path = r"C:\Users\Avani N. Goswami\Desktop\Police AI System\police ai system\people.mp4"
# tracker = PersonTracker()
# state_manager = TrackStateManager

# cap = cv2.VideoCapture(video_path)
# ret, frame = cap.read()
# h,w = frame.shape[:2]
# cap.release()

# box_annonator = sv.BoxAnnotator(thickness=2)

# for result in model.track(source=video_path, stream=True, classes=[0,24,26,28,39,43,67],imgsz=600):
#     frame = result.orig_img
#     detections = sv.Detections.from_ultralytics(result)
#     frame = box_annonator.annotate(scene=frame,detections = detections)
#     cv2.imshow("frame", frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cv2.destroyAllWindows()


from pathlib import Path
import sys

# Ensure project root is on sys.path so local packages (e.g. tracking)
# can be imported when running this file as a script.
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
      sys.path.insert(0, str(project_root))

import cv2
import supervision as sv
from ultralytics import YOLO
from tracking.tracker import PersonTracker
from tracking.track_state import TrackStateManager

model = YOLO("yolov8s.pt")
# model = YOLO("yolov8n.pt")

video_path = r"C:\Users\Avani N. Goswami\Desktop\Police AI System\police ai system\people.mp4"
tracker = PersonTracker()
state_manager = TrackStateManager()

cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()
    if not ret:
          break

    tracked_person = tracker.process_frame(frame=frame)
    state = state_manager.update(tracked_people=tracked_person,)

    for person in tracked_person:
          pid = person['id']
          l,t,r,b = person['bbox']
          label = person['label']


          cv2.rectangle(frame,(l,t),(r,b),color=(0,255,0),thickness=2)
          cv2.putText(frame,f'{label} {pid}',(l,t-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)

    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
            break


cap.release()
cv2.destroyAllWindows()