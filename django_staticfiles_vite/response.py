import urllib.request
from django.http.response import HttpResponse


class ProxyResponse(HttpResponse):
    forbidden_headers = ["Connection"]

    def __init__(self, url, **kwargs):
        try:
            response = urllib.request.urlopen(url)
            kwargs["headers"] = {
                key: value
                for key, value in response.headers.items()
                if key not in self.forbidden_headers
            }
            super().__init__(content=response.read(), **kwargs)
        except Exception as error:
            self.status_code = getattr(error, "code", 500)
            super().__init__(content=getattr(error, "msg", "Unknown"), **kwargs)
