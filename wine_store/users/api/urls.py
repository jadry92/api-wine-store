""" URLs for users endpoints """

# dj_auth_rest

# Django
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

# Rest Framework
from rest_framework.routers import SimpleRouter

# Users
from wine_store.users.api.views import UserAddressViewSet

router = SimpleRouter()
router.register(r"address", UserAddressViewSet, basename="address")

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path(
        "auth/account-confirm-email/",
        TemplateView.as_view(template_name="email_verification.html"),
        name="account_email_verification_sent",
    ),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
] + router.urls
