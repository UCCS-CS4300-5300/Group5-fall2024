from django import template
from home.services import daily_lesson_translation

# used to translate words from lesson templates

register = template.Library()

@register.simple_tag
def translate(word, selected_language):
    translations = daily_lesson_translation(word, selected_language)
    return translations if translations else word