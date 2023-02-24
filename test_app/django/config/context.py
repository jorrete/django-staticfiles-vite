from django.urls import reverse


def my_context():
    return {
        "foo": 3,
        "home": reverse("www:index"),
    }
