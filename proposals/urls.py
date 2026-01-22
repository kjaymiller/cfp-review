from django.urls import path, include
from .views import ProposalView

app_name = "proposals"

urlpatterns = [
    path("my-proposals/", include(ProposalView.get_urls())),
]
