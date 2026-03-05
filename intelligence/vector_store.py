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




# from chromadb import Client
# from chromadb.config import Settings
# from sentence_transformers import SentenceTransformer

# class EventVectorStore:

#     def __init__(self):
#         # Initialize embedding model
#         self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
#         # Initialize Chroma client (in-memory)
#         self.client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="chroma_db"))
#         self.collection = self.client.get_or_create_collection("events")
    
#     def embed_event(self, event_text):
#         # Create embedding
#         embedding = self.model.encode([event_text]).tolist()
        
#         # Use the event text as the unique id
#         self.collection.add(
#             documents=[event_text],
#             ids=[str(len(self.collection.get()['ids']))],
#             embeddings=embedding
#         )
    
#     def search_similar(self, query_text, k=3):
#         query_embedding = self.model.encode([query_text]).tolist()
#         results = self.collection.query(
#             query_embeddings=query_embedding,
#             n_results=k
#         )
#         # results['documents'] is a list of lists (one per query)
#         return results['documents'][0] if results['documents'] else []

#     @staticmethod
#     def event_to_text(event):
#         return (
#             f"{event.event_type} occurred at zone {event.zone} "
#             f"confidence {event.confidence} "
#             f"time {event.timestamp}"
#         )


# import chromadb
# from sentence_transformers import SentenceTransformer
# import uuid

# class EventVectorStore:

#     def __init__(self):
#         self.model = SentenceTransformer("all-MiniLM-L6-v2")

#         # NEW correct Chroma client
#         self.client = chromadb.Client()

#         self.collection = self.client.get_or_create_collection(
#             name="events"
#         )

#     def embed_event(self, event_text):
#         embedding = self.model.encode(event_text).tolist()

#         self.collection.add(
#             documents=[event_text],
#             embeddings=[embedding],
#             ids=[str(uuid.uuid4())]
#         )

#     def search_similar(self, query_text, k=3):
#         query_embedding = self.model.encode(query_text).tolist()

#         results = self.collection.query(
#             query_embeddings=[query_embedding],
#             n_results=k
#         )

#         return results["documents"][0] if results["documents"] else []

#     @staticmethod
#     def event_to_text(event):
#         return (
#             f"{event.event_type} occurred at zone {event.zone} "
#             f"confidence {event.confidence} "
#             f"time {event.timestamp}"
#         )