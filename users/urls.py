from django.urls import path
from .views import UserSettingsView

app_name = "users"

urlpatterns = [
    path("settings/", UserSettingsView.as_view(), name="settings"),
]
