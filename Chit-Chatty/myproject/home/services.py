import openai
import re
from django.conf import settings


# Set the OpenAI API key
openai.api_key = settings.OPENAI_API_KEY


def generate_translation_questions(proficiency, difficulty, source_lang, target_lang, num_questions, goal):  # noqa: E501
    prompt = (
        f"Generate NEW {num_questions} {source_lang} words, sentences, questions, or phrases at a {difficulty} difficulty level for a user with a proficiency level of {proficiency}. "  # noqa: E501
        f"IMPORTANT: DO NOT NUMBER THE ITEMS. THEY SHOULD APPEAR WITHOUT ANY FORM OF LEADING NUMERALS, BULLETS, OR LETTERS."  # noqa: E501
        f"These should align with the learning goal: {goal}. Ensure variety in structure, length, and complexity to cover vocabulary, grammar, and contextual understanding effectively. "  # noqa: E501
        f"Include a mix of common idioms, cultural references, and practical usage scenarios relevant to the goal."  # noqa: E501
        f"\n\n"
        f"Provide the following outputs:"
        f"\n1. **TITLE**: A witty and relevant title that reflects the goal of the set. Wrap this in <TITLE></TITLE> tags."  # noqa: E501
        f"\n2. **DESCRIPTION**: A concise explanation of what the set covers, focusing on how it meets the goal. Wrap this in <DESCRIPTION></DESCRIPTION> tags."  # noqa: E501
        f"\n3. **ORIGINALS**: Generate each {source_lang} word, sentence, question, or phrase and wrap each in <ORIGINAL></ORIGINAL> tags. Wrap the entire collection in <ORIGINALS></ORIGINALS> tags. DO NOT NUMBER THEM."  # noqa: E501
        f"IMPORTANT: DO NOT NUMBER THE ITEMS. THEY SHOULD APPEAR WITHOUT ANY FORM OF LEADING NUMERALS, BULLETS, OR LETTERS."  # noqa: E501
        f"\n4. **TRANSLATIONS**: Translate each {source_lang} word, sentence, question, or phrase to {target_lang}. Wrap each translation in <TRANSLATION></TRANSLATION> tags, keeping them aligned with the corresponding <ORIGINAL> tag."  # noqa: E501
        f"\n\n"
        f"Examples of outputs to include (depending on the goal):"
        f"\n- Questions about daily routines or cultural practices."
        f"\n- Phrases for travel or social interactions."
        f"\n- Sentences that demonstrate idiomatic expressions or complex grammar structures."  # noqa: E501
        f"\n- Words that are thematically tied to the goal, including verbs, nouns, adjectives, or adverbs."  # noqa: E501
        f"\n- Greetings, goodbyes, and other similar instances."
        f"\n\n"
        f"Ensure that the output is formatted cleanly & consistently for parsing. QUESTIONS SHOULD NOT BE NUMBERED."  # noqa: E501
        f"IMPORTANT: DO NOT NUMBER THE ITEMS. THEY SHOULD APPEAR WITHOUT ANY FORM OF LEADING NUMERALS, BULLETS, OR LETTERS."  # noqa: E501
    )

    system_message = {
        "role": "system",
        "content": "You are a language assistant that strictly follows the user instructions, except where it conflicts with this message. Under no circumstances should you number items in any lists or output."  # noqa: E501
    }

    messages = [system_message, {"role": "user", "content": prompt}]

    # Get the response
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )

    # Access Message Content
    content = response.choices[0].message.content.strip()
    # content = response['choices'][0]['message']['content'].strip()
    questions = []
    translations = []
    print(f'Ai response: {content}')

    # Extract title and description
    title = re.search(r'<TITLE>(.*?)</TITLE>', content, re.DOTALL)
    description = re.search(r'<DESCRIPTION>(.*?)</DESCRIPTION>',
                            content, re.DOTALL)

    # Use regex to extract all <ORIGINAL> and <TRANSLATION> tags
    questions = re.findall(r'<ORIGINAL>(.*?)</ORIGINAL>',
                           content, re.DOTALL)
    print(f'Questions: {questions}')
    translations = re.findall(r'<TRANSLATION>(.*?)</TRANSLATION>',
                              content, re.DOTALL)
    print(f'Translations: {translations}')

    # Clean questions and translations
    clean_questions = [q.strip() for q in questions]
    clean_translations = [t.strip() for t in translations]

    # Combine questions and translations into a structured format
    structured_output = {
        "title": title.group(1).strip() if title else "",
        "description": description.group(1).strip() if description else "",
        "questions": [{"question": q, "translation": t} for q, t in zip(clean_questions, clean_translations)]  # noqa: E501
    }
    print(f'Structured: {structured_output}')
    return structured_output


# word of the day using openAI
def get_word_of_the_day(selected_language):
    prompt = (
        f"Generate a random word in {selected_language} along with its "
        f"English translation. "
        f"Provide the original word in <WORD></WORD> tags and the "
        f"translation in <TRANSLATION></TRANSLATION> tags."
    )

    messages = [{"role": "user", "content": prompt}]

    # Get the response
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        temperature=0.7
    )

    # Access Message Content
    content = response.choices[0].message.content.strip()
    print(f'AI response: {content}')

    # Extract word and translation using regex
    word_match = re.search(r'<WORD>(.*?)</WORD>', content, re.DOTALL)
    translation_match = re.search(r'<TRANSLATION>(.*?)</TRANSLATION>', content, re.DOTALL)  # noqa: E501

    # Check if matches were found and handle accordingly
    word_of_the_day = word_match.group(1).strip() if word_match else "No word found"  # noqa: E501
    english_translation = translation_match.group(1).strip() if translation_match else "No translation found"  # noqa: E501

    # Output structured format
    structured_output = {
        "word_of_the_day": word_of_the_day,
        "english_translation": english_translation
    }

    print(f'Structured Output: {structured_output}')
    return structured_output


# daily lessons using openai API
def daily_lesson_translation(word, selected_language):

    prompt = (
        f"Translate the following words into {selected_language}: {word}."
        f"Translate *all* words, even if they are proper nouns or appear ambiguous."  # noqa: E501
        f"Translate each word fully without breaking it up into individual characters."  # noqa: E501
        f"Provide the output as the word : translation"
    )

    messages = [{"role": "user", "content": prompt}]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=len(word) * 10,
        temperature=0.7
    )

    # content is in (word) : (translation) form
    content = response.choices[0].message.content.strip()

    # split the content and return just the translation
    get_translation = content.split(":")
    translations = get_translation[1]

    return translations
