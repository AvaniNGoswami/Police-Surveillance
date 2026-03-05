from apscheduler.schedulers.background import BackgroundScheduler
from intelligence.summarizer import ShiftSummarizer
from intelligence.vector_store import EventVectorStore

def start_scheduler():
    vector_store = EventVectorStore()
    summarizer = ShiftSummarizer(vector_store)

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        summarizer.summary,
        'cron',
        minute=0
    )

    scheduler.start()
    print('Scheduler started.🔥🔥🔥🔥')
    return scheduler