from intelligence.summarizer import ShiftSummarizer
from fastapi import APIRouter
from intelligence.vector_store import EventVectorStore

router = APIRouter(prefix='/summary', tags=['Summary'])
vector_store = EventVectorStore()

@router.get('/')
def get_summary():
    summarizer = ShiftSummarizer(vector_store)
    return {"summary": summarizer.summary()}