from django.conf import settings
from django.utils.translation import get_language

def get_lang():
    return (get_language() or settings.LANGUAGE_CODE)[:2]

def get_order_by_title():
    if get_lang() == 'el':
        return 'title_gr'
    else:
        return 'title_en'

def get_order_by_display_name():
    if get_lang() == 'el':
        return 'display_name'
    else:
        return 'display_name_en'