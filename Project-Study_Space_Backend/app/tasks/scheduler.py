from apscheduler.schedulers.background import BackgroundScheduler
from app.services.no_show import process_no_show_bookings
from app.core.database import SessionLocal

scheduler = BackgroundScheduler()

def auto_no_show_job():
    db = SessionLocal()
    try:
        process_no_show_bookings(db)
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(auto_no_show_job, "interval", minutes=1)
    scheduler.start()
