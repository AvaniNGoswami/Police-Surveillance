from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional,Dict
from uuid import uuid4
from app.models.event import Event
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.database import engine
from sqlalchemy import func

class event_record(BaseModel):
    camera_id : str  
    event_type: str
    confidence: float
    zone: Optional[str] = None
    image_path: Optional[str] = None
    metadata_json: Optional[Dict] = None
    resolved: Optional[bool] = None


router = APIRouter(prefix='/event',tags=['Event'])

@router.post('/events')
def record_event(data:event_record):
    with Session(engine) as session:
        event = Event(
            id = str(uuid4()),
            timestamp = datetime.utcnow(),
            camera_id = data.camera_id,
            event_type = data.event_type,
            confidence = data.confidence,
            zone = data.zone,
            image_path = data.image_path,
            metadata_json = data.metadata_json,
            resolved = data.resolved
        )
        session.add(event)
        session.commit()
        session.refresh(event)
    return {'status':'ok','event':event}


@router.get('get_events')
def get_event():
    with Session(engine) as session:
        event = session.query(Event).all()
    return event

@router.get('hour_summary')
def get_summary():
    result=[]
    hour = func.date_trunc('hour',Event.timestamp).label('hour')
    with Session(engine) as session:
        summary = session.query(hour,Event.event_type,func.count()).group_by('hour',Event.event_type).all()
        for hour,event_type,count in summary:
            result.append({'hour':hour,'event_type':event_type,'count':count})
    return result
    