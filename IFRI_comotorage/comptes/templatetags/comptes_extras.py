from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.filter
def get_initials(user):
    if not user:
        return ''
    initials = ''
    if user.first_name:
        initials += user.first_name[0]
    if user.last_name:
        initials += user.last_name[0]
    return initials.upper() if initials else user.username[0].upper()

@register.filter
def get_full_name(user):
    if not user:
        return ''
    if user.first_name and user.last_name:
        return f"{user.first_name} {user.last_name}"
    return user.username 