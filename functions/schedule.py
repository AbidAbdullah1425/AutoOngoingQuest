import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

    def schedule_task(self, task_func, interval_minutes=10):
        self.scheduler.add_job(
            task_func,
            'interval',
            minutes=interval_minutes,
            next_run_time=datetime.now()
        )

    def start(self):
        self.scheduler.start()
