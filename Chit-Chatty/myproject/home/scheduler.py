from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from .tasks import resetStreak 
from .models import LastStreakReset
from django.utils import timezone


def startScheduler():

    # Initialize the background scheduler
    scheduler = BackgroundScheduler()

    # Schedule the resetStreak function to run daily at midnight
    scheduler.add_job(
        resetStreak,
        trigger=CronTrigger(hour=0, minute=0),
        #trigger=CronTrigger(minute='*'),  RUNS EVERY MINUTE. USE FOR TESTING
        id="reset_streak_job",
        replace_existing=True,
    )

    ''' 
    This section for forcing a reset is only here because our server doesn't run 24/7
    '''
    # Get the last time when streak was reset 
    lastResetTime, created = LastStreakReset.objects.get_or_create()

    # Check if the current date is different from the last execution date
    currentTime = timezone.now()
    
    # If the current date is after the last run date, run the resetStreak function
    if currentTime.date() > lastResetTime.lastReset.date():
        resetStreak()  # Run the function to reset the streak
        lastResetTime.lastReset = currentTime  # Update the last run time
        lastResetTime.save()  # Save the log entry

    # Start the scheduler to being running the scheduled jobs in the background
    scheduler.start()
    print("Scheduler has started")