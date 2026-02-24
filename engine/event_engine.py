import time
import math
from collections import defaultdict

class EventEngine:
    def __init__(self,loiter_radius=30,loiter_time=15):
        self.loiter_radius = loiter_radius
        self.loiter_time = loiter_time
        self.loittering_flag = {}
        self.bag_links = {}
        self.unattended_flags = {}
        self.bag_timer = {}
        self.zone_history = defaultdict(list)
        self.surge_flag = {}

    def detect_loiter(self,tracks):
        current_time = time.time()
        for pid,data in tracks.items():
            if data['label']!='person':
                continue

            position = list(data['position'])
            if len(position)<30:
                continue

            cx = sum(p[0] for p in position) / len(position)
            cy = sum(p[1] for p in position) / len(position)

            max_dist = max_dist = max(
                                        math.sqrt((p[0]-cx)**2 + (p[1]-cy)**2)
                                        for p in position
                                    )

            time_diff = current_time - data['first_seen']

            if max_dist<self.loiter_radius and time_diff>self.loiter_time:
                if pid not in self.loittering_flag:
                    self.loittering_flag[pid]=True
                    print(f"[{time.strftime('%H:%M:%S')}] LOITERING detected person {pid}")


    def detect_unattempted(self,tracked):
        current_time = time.time()

        person = {pid:data for pid,data in tracked.items() if data['label']=='person'}
        obj = {pid:data for pid,data in tracked.items() if data['label'] in ['backpack','handbag', 'suitcase', 'bottle', 'knife', 'cell phone']}

        for bid,data in obj.items():
            o_pos = data['position'][-1]
            min_dist = float('inf')
            near_person = None
            for pid,pdata in person.items():
                pos = pdata['position'][-1]
                distance = math.dist(pos,o_pos)
                if distance <min_dist:
                    min_dist = distance
                    near_person = pid
            
            if min_dist<100:
                self.bag_links[bid] = near_person
                self.bag_timer.pop(bid, None)

            else:
                if bid not in self.bag_timer:
                    self.bag_timer[bid] = current_time
                
                time_diff = current_time - self.bag_timer[bid]

                if time_diff>20:
                    if bid not in self.unattended_flags:
                        self.unattended_flags[bid] = True
                        print(f"[{time.strftime('%H:%M:%S')}] UNATTENDED BAG detected id {bid}")


    def detect_crowd_surge(self, tracks, frame_width, frame_height):
        zone_count = {}

        for i in range(3):
            for j in range(3):
                zone_count[(i,j)]=0
        
        zone_w = frame_width // 3
        zone_h = frame_height // 3

        for pid,data in tracks.items():
            if data['label']!='person':
                continue
            x,y = data['position'][-1]
            zone_x = min(x // zone_w, 2)
            zone_y = min(y // zone_h, 2)
            zone_count[(zone_x,zone_y)]+=1

        current_time = time.time()

        for zone,count in zone_count.items():
            self.zone_history[zone].append((current_time,count))

            self.zone_history[zone]=[
                (t,c) for (t,c) in self.zone_history[zone]
                if current_time-t<20
            ]

            if len(self.zone_history[zone])>5:
                before = self.zone_history[zone][0][1]
                after = count
                if before > 0 and after>before*2:
                    if zone not in self.surge_flag:
                        self.surge_flag[zone] = True
                        print(f"[{time.strftime('%H:%M:%S')}] CROWD SURGE zone {zone}")
                    
    

