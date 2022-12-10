from re import compile

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from ..settings import VITE_BUNDLE_KEYWORD, VITE_PORT
from ..utils import get_bundle_css_name, normalize_extension, path_is_vite_bunlde

register = template.Library()


def build_vite_url(name):
    return f"http://localhost:{VITE_PORT}{settings.STATIC_URL}{name}"


@register.simple_tag
def vite_hrm(*args):
    if not settings.DEBUG:
        return ""

    path = f"http://localhost:{VITE_PORT}/@vite/client"

    return mark_safe(f'<script type="module" src="{path}"></script>')


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
            f'Missing vite bundle keyworkd "{VITE_BUNDLE_KEYWORD}" for static path: {name}'
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
                f'<script src="{path}" type="module"{" defer" if defer else ""}></script>',
                (
                    f'<link href="{vite_static(get_bundle_css_name(normalize_extension(name)))}" rel="stylesheet">'
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
        f"<link href=\"{path}\" rel=\"stylesheet\"{' defer' if defer else ''}>"
    )
