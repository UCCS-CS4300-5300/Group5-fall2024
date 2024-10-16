from django.core.management.base import BaseCommand
from home.models import Question, Quiz

class Command(BaseCommand):
    help = 'Adds easy translation questions to the database'

    def handle(self, *args, **kwargs):
        # Fetch the first quiz (or specify another quiz)
        quiz = Quiz.objects.first()  

        if not quiz:
            self.stdout.write(self.style.ERROR("No quiz found"))
            return

        # Define three easy questions
        questions = [
            {
                "translation_question": "Hola", 
                "correct_answer": "Hello",
                "source_language": "Spanish",
                "target_language": "English",
                "difficulty": "Easy"
            },
            {
                "translation_question": "Gracias", 
                "correct_answer": "Thank you",
                "source_language": "Spanish",
                "target_language": "English",
                "difficulty": "Easy"
            },
            {
                "translation_question": "Adiós", 
                "correct_answer": "Goodbye",
                "source_language": "Spanish",
                "target_language": "English",
                "difficulty": "Easy"
            }
        ]

        # Loop through and add the questions to the database
        for question_data in questions:
            Question.objects.create(
                quiz=quiz,
                translation_question=question_data["translation_question"],
                correct_answer=question_data["correct_answer"],
                source_language=question_data["source_language"],
                target_language=question_data["target_language"],
                difficulty=question_data["difficulty"]
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully added {len(questions)} easy questions"))
