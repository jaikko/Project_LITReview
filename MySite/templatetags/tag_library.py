from django import template
register = template.Library()


@register.filter()
def to_int(value):
    return int(value)


@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)
