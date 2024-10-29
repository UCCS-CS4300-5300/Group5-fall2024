from .models import Member
import logging

'''
Task that will execute everyday at midnight to reset the streak counter for users who haven't done anything for a day
'''
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def resetStreak():
    logger.info("resetStreak function triggered.")
    # Get all the members registered on the application
    members = Member.objects.all()

    # Go through all members. If they haven't completed a quiz for the entire day, reset streak count to 0 
    for member in members:
        if member.hasCompletedQuiz == False:
            member.streakCount = 0
            
        # Reset variable for next day
        member.hasCompletedQuiz = False
        member.save()