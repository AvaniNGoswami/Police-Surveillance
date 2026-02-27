from app.router.event_router import router as event_router
from app.router.summary import router as summary
from fastapi import FastAPI
import sys
print(sys.executable)
print(sys.path)

app = FastAPI(title='Police Servillience system')

@app.get('/')
def health_check():
    return {'msg' : 'Welcome to Police Servillience System'}


app.include_router(event_router)
app.include_router(summary)