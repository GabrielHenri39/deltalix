from django import template
import os

register = template.Library()

@register.filter(name='endswith')
def endswith(value, suffix):
    """Check if a string ends with the given suffix."""

    if not value:
        return False
    return str(value).endswith(str(suffix).lower())
@register.filter(name='basename')
def basename(value):
    """Get the base name of a file path."""
    if not value:
        return ''
    return os.path.basename(value)