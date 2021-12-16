import inspect

import markdown as _markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown(value):
    return mark_safe(_markdown.markdown(inspect.cleandoc(value).strip()))
