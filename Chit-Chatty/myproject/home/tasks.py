from .models import Member, WordOfTheDayTracker
import logging


'''
Daily midnight execution to reset the streak counter if condtns met
'''
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def resetStreak():
    logger.info("resetStreak function triggered.")
    # Get all the members registered on the application
    members = Member.objects.all()

    # Go through all members.
    # If daily quiz not completed, reset streak count to 0
    for member in members:
        if member.hasCompletedQuiz == False:
            member.streakCount = 0

        # Reset variable for next day
        member.hasCompletedQuiz = False
        member.save()


def resetWOTDTrackers():
    logger.info("resetWOTDTrackers function triggered.")
    # Get all the members registered on the application
    members = Member.objects.all()

    # Go through all members.
    # Clear tracking lists for the word of the day
    for member in members:
        wotd_tracker = WordOfTheDayTracker.objects.get(member=member)
        wotd_tracker.languagesGenerated = ""
        wotd_tracker.languagesCompleted = ""
        wotd_tracker.save()
