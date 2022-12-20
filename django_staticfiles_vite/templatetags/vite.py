from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from ..settings import VITE_BUNDLE_KEYWORD, VITE_PORT
from ..utils import get_bundle_css_name, normalize_extension, path_is_vite_bunlde

register = template.Library()


@register.simple_tag
def vite_static(name, **kwargs):
    if not settings.DEBUG:
        name = normalize_extension(name)
        return static(name)

    return (
        f"http://localhost:{VITE_PORT}{'' if name[0] == '/' else settings.STATIC_URL}{name}"
    )


@register.simple_tag
def vite_hrm(**kwargs):
    return (
        '<script type="module"'
        f' src="http://localhost:{VITE_PORT}/@vite/client"></script>'
    )


@register.simple_tag
def vite_script(name, **kwargs):
    """ """
    if not path_is_vite_bunlde(name):
        raise Exception(
            f'Missing vite bundle keyworkd "{VITE_BUNDLE_KEYWORD}" for static path:'
            f" {name}"
        )

    hrm = kwargs.get("hrm", True)
    defer = kwargs.get("defer", False)
    style = kwargs.get("style", False) and not settings.DEBUG
    path = vite_static(name)

    return mark_safe(
        "\n".join(
            [
                (vite_hrm() if hrm and settings.DEBUG else ""),
                (
                    f'<script src="{path}"'
                    f' type="module"{" defer" if defer else ""}></script>'
                ),
                (
                    "<link"
                    f' href="{vite_static(get_bundle_css_name(normalize_extension(name)))}"'
                    ' rel="stylesheet">'
                    if style
                    else ""
                ),
            ]
        )
    )


@register.simple_tag
def vite_style(name, **kwargs):
    """ """
    if not path_is_vite_bunlde(name):
        raise Exception(
            f'Missing vite bundle keyworkd "{VITE_BUNDLE_KEYWORD}" for static path:'
            f" {name}"
        )

    path = vite_static(name)

    return mark_safe(f'<link href="{path}" rel="stylesheet">')
