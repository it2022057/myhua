from datetime import datetime, date

from django import template
from django.db.models.fields.files import ImageFieldFile
from django.db.models.manager import BaseManager
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from core.views import DEFAULT_CONTEXT_VALUES
from hua_cbms import settings

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """
    Supports dotted paths, callables, translations and ManyToMany fields:
    'candidate.program.title'
    'participants.display_name_full'
    """
    lang = get_language()[:2]
    parts = attr.split(".")

    for part in parts:
        if obj is None:
            return ""

        prev_obj = obj
        obj = getattr(obj, part, "")

        # Handle ManyToMany / related managers
        if isinstance(obj, BaseManager):
            new_part = ".".join(parts[parts.index(part) + 1:])

            if new_part:
                return mark_safe(
                    "<br>".join(
                        str(get_attr(o, new_part))
                        for o in obj.all()
                    )
                )
            return mark_safe("<br>".join(str(o) for o in obj.all()))

        if callable(obj):
            obj = obj()

    # Check for translation
    if isinstance(obj, str) and part:

        if lang == 'en':
            new_part = part + '_en'
            if hasattr(prev_obj, new_part):
                return get_attr(prev_obj, new_part)

            elif part.endswith('_gr'):
                new_part = part.split('_gr')[0] + '_en'
                if hasattr(prev_obj, new_part):
                    return getattr(prev_obj, new_part)

    # Format datetime fields
    if isinstance(obj, datetime):
        if timezone.is_aware(obj):
            obj = timezone.localtime(obj)

        if lang == 'en':
            # e.g. July 22, 2026, 2:30 pm and August 17, 2027, 12:30 am
            return obj.strftime('%B %-d, %Y, %-I:%M %P')

        # e.g. Ιούλιος 22, 2026, 2:30 μ.μ. και Αύγουστος 30, 2027, 9:30 π.μ.
        return (
            f"{date_format(obj, 'F', use_l10n=True)} "
            f"{obj.day}, "
            f"{obj.year}, "
            f"{obj.strftime('%-I:%M')} "
            f"{'π.μ.' if obj.hour < 12 else 'μ.μ.'}"
        )
    # Format date fields
    elif isinstance(obj, date):
        # e.g. 25/02/2006
        return obj.strftime(settings.DATE_FORMAT)

    return obj

@register.filter
def get_item(d, key):
    return d.get(key)

@register.filter
def get_items(d):
    keys, vals = d.items()
    return vals

@register.inclusion_tag("core/partials/table.html")
def render_table(table):
    context = {}
    for key in DEFAULT_CONTEXT_VALUES.keys():
        context[key] = table.get(key, '')
    return context

@register.inclusion_tag("core/partials/section.html")
def render_section(section):
    context = {}
    for key in section.keys():
        context[key] = section.get(key, '')

    return context

@register.filter
def get_filename(s):
    filename = str(s.value()).split('/')[-1]
    if len(filename) > 20:
        filename = filename[0:16] + '...'
    return filename

@register.simple_tag
def media_download_url(file):
    if not file:
        return ''

    return reverse('media_download', kwargs={'path': file.name})

@register.filter
def is_image(obj):
    return isinstance(obj, ImageFieldFile)

@register.filter
def has_image(obj):
    return bool(obj.name)
