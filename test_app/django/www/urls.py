from django.urls import path

from .views import index

app_name = "wwww"

urlpatterns = [
    path("", index, name="index"),
]
