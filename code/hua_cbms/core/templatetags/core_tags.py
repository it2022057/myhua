from django import template
from django.db.models.fields.files import ImageFieldFile
from django.db.models.manager import BaseManager
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from core.views import DEFAULT_CONTEXT_VALUES

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

@register.filter
def is_image(obj):
    return isinstance(obj, ImageFieldFile)

@register.filter
def has_image(obj):
    return bool(obj.name)
