from django.core.management.base import BaseCommand
from home.models import Question

class Command(BaseCommand):
    help = 'Adds translation questions to the database for all difficulties'

    def handle(self, *args, **kwargs):

        # Define the questions for all difficulty levels
        questions = [
            # Easy questions
            {
                "translation_question": "Hola", 
                "correct_answer": "Hello",
                "difficulty": "Easy"
            },
            {
                "translation_question": "Gracias", 
                "correct_answer": "Thank you",
                "difficulty": "Easy"
            },
            {
                "translation_question": "Adiós", 
                "correct_answer": "Goodbye",
                "difficulty": "Easy"
            },
            {
                "translation_question": "Por favor", 
                "correct_answer": "Please",
                "difficulty": "Easy"
            },
            {
                "translation_question": "Sí", 
                "correct_answer": "Yes",
                "difficulty": "Easy"
            },
            {
                "translation_question": "No", 
                "correct_answer": "No",
                "difficulty": "Easy"
            },
            {
                "translation_question": "Hasta luego", 
                "correct_answer": "See you later",
                "difficulty": "Easy"
            },
            {
                "translation_question": "¿Cómo estás?", 
                "correct_answer": "How are you?",
                "difficulty": "Easy"
            },
            {
                "translation_question": "Buenos días", 
                "correct_answer": "Good morning",
                "difficulty": "Easy"
            },
            {
                "translation_question": "Buenas noches", 
                "correct_answer": "Good night",
                "difficulty": "Easy"
            },

            # Medium questions
            {
                "translation_question": "Estoy aprendiendo español", 
                "correct_answer": "I am learning Spanish",
                "difficulty": "Medium"
            },
            {
                "translation_question": "¿Dónde está el baño?", 
                "correct_answer": "Where is the bathroom?",
                "difficulty": "Medium"
            },
            {
                "translation_question": "¿Puedes ayudarme?", 
                "correct_answer": "Can you help me?",
                "difficulty": "Medium"
            },
            {
                "translation_question": "Hace calor hoy", 
                "correct_answer": "It's hot today",
                "difficulty": "Medium"
            },
            {
                "translation_question": "Estoy cansado", 
                "correct_answer": "I am tired",
                "difficulty": "Medium"
            },
            {
                "translation_question": "¿Cuánto cuesta esto?", 
                "correct_answer": "How much does this cost?",
                "difficulty": "Medium"
            },
            {
                "translation_question": "Vivo en los Estados Unidos", 
                "correct_answer": "I live in the United States",
                "difficulty": "Medium"
            },
            {
                "translation_question": "Me gusta mucho este lugar", 
                "correct_answer": "I really like this place",
                "difficulty": "Medium"
            },
            {
                "translation_question": "¿Qué hora es?", 
                "correct_answer": "What time is it?",
                "difficulty": "Medium"
            },
            {
                "translation_question": "Estoy buscando un restaurante", 
                "correct_answer": "I am looking for a restaurant",
                "difficulty": "Medium"
            },

            # Hard questions
            {
                "translation_question": "Tengo que hacer una llamada importante", 
                "correct_answer": "I have to make an important call",
                "difficulty": "Hard"
            },
            {
                "translation_question": "Este libro es difícil de entender", 
                "correct_answer": "This book is hard to understand",
                "difficulty": "Hard"
            },
            {
                "translation_question": "¿Podrías darme más detalles sobre el evento?", 
                "correct_answer": "Could you give me more details about the event?",
                "difficulty": "Hard"
            },
            {
                "translation_question": "Estamos planificando un viaje para la próxima semana", 
                "correct_answer": "We are planning a trip for next week",
                "difficulty": "Hard"
            },
            {
                "translation_question": "¿Cuál es la mejor manera de llegar al aeropuerto?", 
                "correct_answer": "What is the best way to get to the airport?",
                "difficulty": "Hard"
            },
            {
                "translation_question": "No entiendo lo que estás tratando de decir", 
                "correct_answer": "I don't understand what you're trying to say",
                "difficulty": "Hard"
            },
            {
                "translation_question": "Este es un problema complicado de resolver", 
                "correct_answer": "This is a complicated problem to solve",
                "difficulty": "Hard"
            },
            {
                "translation_question": "¿Cuáles son tus planes para el futuro?", 
                "correct_answer": "What are your plans for the future?",
                "difficulty": "Hard"
            },
            {
                "translation_question": "Lo siento, no tengo tiempo en este momento", 
                "correct_answer": "Sorry, I don't have time right now",
                "difficulty": "Hard"
            },
            {
                "translation_question": "Estoy buscando una solución a este problema", 
                "correct_answer": "I am looking for a solution to this problem",
                "difficulty": "Hard"
            }
        ]

        # Loop through and add the questions to the database
        for question_data in questions:
            Question.objects.create(
                translation_question=question_data["translation_question"],
                correct_answer=question_data["correct_answer"],
                source_language="Spanish",  # All questions are in Spanish
                target_language="English",  # Translations are expected in English
                difficulty=question_data["difficulty"]
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully added {len(questions)} questions for all difficulties"))
