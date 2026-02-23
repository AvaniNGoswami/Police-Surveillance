import time
from collections import deque

class TrackStateManager:
    def __init__(self,history_sec=10, fps=30):
        self.history_length = history_sec * fps
        self.tracks = {}

    def update(self, tracked_people):
        current_time = time.time()
        for person in tracked_people:
            pid = person['id']
            label = person['label']
            l,t,r,b = person['bbox']
            centre = ((l + r) // 2, (t + b) // 2)
            if pid not in self.tracks:
                self.tracks[pid] = {
                    'label':label,
                    'position': deque(maxlen=self.history_length),
                    'first_seen':current_time
                }
            self.tracks[pid]['position'].append(centre)
        
        return self.tracks