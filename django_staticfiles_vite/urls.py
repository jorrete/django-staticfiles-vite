from django.urls import path

from .views import qunit_list_view, qunit_test_view

urlpatterns = [
    path("qunit/", qunit_list_view),
    path("qunit/test/", qunit_test_view),
]
