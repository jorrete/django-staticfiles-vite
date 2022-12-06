from re import compile

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from ..settings import VITE_BUNDLE_KEYWORD, VITE_PORT
from ..utils import clean_bundle_name, path_is_vite_bunlde

register = template.Library()
regexp = compile(
    "vite_\\w+\\s+[\"'](\\w+\\.{0}\\.\\w+)[\"']".format(VITE_BUNDLE_KEYWORD)
)


def build_vite_url(name):
    return "http://localhost:{}/{}".format(VITE_PORT, name)


@register.simple_tag
def vite_hrm(*args):
    if not settings.DEBUG:
        return ""

    path = build_vite_url("@vite/client")

    return mark_safe('<script type="module" src="{}"></script>'.format(path))


@register.simple_tag
def vite_static(name):
    """
    Join the given path with the STATIC_URL setting.
    Usage::
        {% static path [as varname] %}
    Examples::
        {% static "myapp/css/base.css" %}
        {% static variable_with_path %}
        {% static "myapp/css/base.css" as admin_base_css %}
        {% static variable_with_path as varname %}
    """
    if not path_is_vite_bunlde(name):
        raise Exception(
            'Missing vite bundle keyworkd "{0}" for static path: {1}'.format(
                VITE_BUNDLE_KEYWORD, name
            )
        )

    if not settings.DEBUG:
        name = clean_bundle_name(name)
        return static(name)

    return "http://localhost:{}/{}".format(VITE_PORT, name)


@register.simple_tag
def vite_script(name, **kwargs):
    """ """
    defer = kwargs.get("defer", False)
    style = kwargs.get("style", False)

    path = vite_static(name)

    return mark_safe(
        "\n".join(
            [
                '<script src="{}" type="module"{}></script>'.format(
                    path,
                    " defer" if defer else "",
                ),
                (
                    '<link href="{}" rel="stylesheet">'.format(path + ".css")
                    if (style and not settings.DEBUG)
                    else ""
                ),
            ]
        )
    )


@register.simple_tag
def vite_style(name, **kwargs):
    """ """
    defer = kwargs.get("defer", False)

    path = vite_static(name)

    return mark_safe(
        '<link href="{}" rel="stylesheet"{}>'.format(path, " defer" if defer else "")
    )
