from django import template
import markdown

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')


@register.filter
def lower(value):
    return value.lower()


@register.filter
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text, safe_mode='escape')


@register.filter()
def template_range(num, num_ranges):
    num_start = num // num_ranges * num_ranges
    num_end = num_start + num_ranges
    return range(num_start + 1, num_end + 1)
