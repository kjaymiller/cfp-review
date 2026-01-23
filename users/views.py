from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import UserSettingsForm


class UserSettingsView(LoginRequiredMixin, UpdateView):
    form_class = UserSettingsForm
    template_name = "users/settings.html"
    success_url = reverse_lazy("users:settings")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your settings have been updated.")
        return super().form_valid(form)
