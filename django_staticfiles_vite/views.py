"""
Views and functions for serving static files. These are only to be used during
development, and SHOULD NOT be used in a production setting.

"""
from .response import ProxyResponse
from .utils import get_proxy_url


def serve_vite(request, **kwargs):
    """
    Serve from proxy server.
    """
    return ProxyResponse(get_proxy_url(request), **kwargs)
