from django.urls import path, re_path

from .views import index, test

urlpatterns = [
    path("", index),
    re_path(r"^vite_test/(?P<test>[\w./]+)$", test),
]
