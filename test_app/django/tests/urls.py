from django.urls import path, re_path

from .views import index, test

app_name = "tests"

urlpatterns = [
    path("", index, name="index"),
    re_path(r"^vite_test/(?P<test>[\w./]+)$", test, name="test"),
]
