# https://chatgpt.com/share/671ad8cb-0dcc-8003-b9df-ae777d2c402d

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_translation_questions(difficulty, source_lang, target_lang, num_questions):
    prompt = f"Generate {num_questions} sentences in {source_lang} to be translated to {target_lang} with {difficulty} difficulty. Provide only the sentences without additional text."

    response = openai.completions.create(
        model="gpt-3.5-turbo",  # or another model you prefer
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None
    )
    
    # Split the response into sentences and remove any extraneous whitespace
    questions = response['choices'][0]['message']['content'].strip().split('\n')
    
    # Filter out any empty lines, just in case
    questions = [q.strip() for q in questions if q.strip()]
    
    return questions


def translate_sentence(sentence, source_lang, target_lang):
    prompt = f"Translate the following sentence from {source_lang} to {target_lang}: '{sentence}'"
    
    response = openai.completions.create(
        model="gpt-3.5-turbo",  # or another model you prefer
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None
    )
    
    # Get the translated text from the response
    translated_sentence = response['choices'][0]['message']['content'].strip()
    
    return translated_sentence