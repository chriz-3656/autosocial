import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)

class AutoSocialScheduler:
    def __init__(self, brain_orchestrator):
        self.scheduler = AsyncIOScheduler()
        self.brain = brain_orchestrator
        
    def start(self):
        # Schedule the post generation task to run every day at 10 AM
        self.scheduler.add_job(
            self.generate_daily_post,
            'cron',
            hour=10,
            minute=0
        )
        self.scheduler.start()
        logger.info("Scheduler started.")
        
    async def generate_daily_post(self):
        logger.info("Running daily post generation...")
        await self.brain.create_and_queue_post("Motivation", [])
