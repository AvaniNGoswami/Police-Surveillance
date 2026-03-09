import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class EventVectorStore:

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(384)
        self.events = []

    def embed_event(self, event_text):

        embedding = self.model.encode([event_text])
        self.index.add(np.array(embedding).astype("float32"))
        self.events.append(event_text)

    def search_similar(self, query_text, k=3):

        query_vec = self.model.encode([query_text])
        D, I = self.index.search(np.array(query_vec).astype("float32"), k)

        return [self.events[i] for i in I[0] if i < len(self.events)]

    def event_to_text(event):
        return (
            f"{event.event_type} occurred at zone {event.zone} "
            f"confidence {event.confidence} "
            f"time {event.timestamp}"
        )

