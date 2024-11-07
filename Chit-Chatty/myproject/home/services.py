import openai
import re
from django.conf import settings

# Set the OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

def generate_translation_questions(difficulty, source_lang, target_lang, num_questions, goal):
    prompt = (
        f"Generate {num_questions} {source_lang} sentences, questions, phrases, or words at a(n) {difficulty} difficulty level."
        f"The context for these questions is the learning goal: {goal}."
        f"Provide a TITLE and DESCRIPTION for the set of questions. The TITLE should be witty and relevant to the goal, and the DESCRIPTION should briefly but accurately explain what the set covers."
        f"Output the title within <TITLE></TITLE> tags and the description within <DESCRIPTION></DESCRIPTION> tags. "
        f"Output each original sentence within <ORIGINAL></ORIGINAL> tags, and wrap the entire set within <ORIGINALS></ORIGINALS> tags. "
        f"Translate these sentences to {target_lang} without pronunciation. Output each translation within <TRANSLATION></TRANSLATION> tags."
    )

    messages = [{"role": "user", "content": prompt}]

    # Get the response
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    # Access Message Content
    content = response.choices[0].message.content.strip()
    questions = []
    translations = []
    print(f'Ai response: {content}')

    # Extract title and description
    title = re.search(r'<TITLE>(.*?)</TITLE>', content, re.DOTALL)
    description = re.search(r'<DESCRIPTION>(.*?)</DESCRIPTION>', content, re.DOTALL)

    # Use regex to extract all <ORIGINAL> and <TRANSLATION> tags
    questions = re.findall(r'<ORIGINAL>(.*?)</ORIGINAL>', content, re.DOTALL)
    print('Questions: {questions}')
    translations = re.findall(r'<TRANSLATION>(.*?)</TRANSLATION>', content, re.DOTALL)
    print('Translations: {translations}')

    clean_questions = [q.replace("<ORIGINAL>", "").replace("</ORIGINAL>", "").strip() for q in questions]
    clean_translations = [t.replace("<TRANSLATION>", "").replace("</TRANSLATION>", "").strip() for t in translations]

    # Combine questions and translations into a structured format
    structured_output = {
        "title": title.group(1).strip() if title else "",
        "description": description.group(1).strip() if description else "",
        "questions": [{"question": q, "translation": t} for q, t in zip(clean_questions, clean_translations)]
    }
    print('Structured: {structured_output}')
    return structured_output
