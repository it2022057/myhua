from django import template

from accounts.checks import is_secretariat, is_staff_member

register = template.Library()

@register.filter(name="is_secretariat")
def test_sec(user):
    return is_secretariat(user)

@register.filter(name="is_staff_member")
def test_staff_member(user):
    return is_staff_member(user)

    