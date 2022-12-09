from re import compile

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage

from ..settings import VITE_BUNDLE_KEYWORD, VITE_PORT
from ..utils import normalize_extension, path_is_vite_bunlde, get_bundle_css_name

register = template.Library()
regexp = compile(
    "vite_\\w+\\s+[\"'](\\w+\\.{0}\\.\\w+)[\"']".format(VITE_BUNDLE_KEYWORD)
)


def build_vite_url(name):
    return "http://localhost:{}{}{}".format(VITE_PORT, settings.STATIC_URL, name)


@register.simple_tag
def vite_hrm(*args):
    if not settings.DEBUG:
        return ""

    path = "http://localhost:{}/{}".format(VITE_PORT, "@vite/client")

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
        name = normalize_extension(name)
        return static(name)

    return build_vite_url(name)


@register.simple_tag
def vite_script(name, **kwargs):
    """ """
    defer = kwargs.get("defer", False)
    style = kwargs.get("style", False) and not settings.DEBUG
    path = vite_static(name)

    return mark_safe(
        "\n".join(
            [
                '<script src="{}" type="module"{}></script>'.format(
                    path,
                    " defer" if defer else "",
                ),
                (
                    '<link href="{}" rel="stylesheet">'.format(
                        vite_static(
                            get_bundle_css_name(
                                normalize_extension(name)
                            )
                        )
                    )
                    if style
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
