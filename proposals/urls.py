from django.urls import path
from .views import (
    ProposalListView,
    ProposalCreateView,
    ProposalUpdateView,
    ProposalDetailView,
)

app_name = "proposals"

urlpatterns = [
    path("", ProposalListView.as_view(), name="list"),
    path("new/", ProposalCreateView.as_view(), name="create"),
    path("<int:pk>/", ProposalDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", ProposalUpdateView.as_view(), name="update"),
]
