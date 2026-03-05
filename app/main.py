from app.router.event_router import router as event_router
from app.router.summary import router as summary
from fastapi import FastAPI
import sys
from app.scheduler import start_scheduler

print(sys.executable)
print(sys.path)

app = FastAPI(title='Police Servillience system')

@app.get('/')
def health_check():
    return {'msg' : 'Welcome to Police Servillience System'}


app.include_router(event_router)
app.include_router(summary)



scheduler = None

@app.on_event("startup")
def startup_event():
    global scheduler
    scheduler = start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

    