from app.router.event_router import router as event_router
from fastapi import FastAPI
app = FastAPI(title='Police Servillience system')

@app.get('/')
def health_check():
    return {'msg' : 'Welcome to Police Servillience System'}


app.include_router(event_router)