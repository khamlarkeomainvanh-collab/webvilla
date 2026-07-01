from django import template

register = template.Library()

@register.filter
def dotformat(value):
    """Format a number with dots as thousand separators: 50000 → 50.000"""
    try:
        n = int(round(float(value)))
        return '{:,}'.format(n).replace(',', '.')
    except (ValueError, TypeError):
        return value
