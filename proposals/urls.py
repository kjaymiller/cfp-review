from django.urls import path
from .views import (
    ProposalListView,
    ProposalCreateView,
    ProposalUpdateView,
    ProposalDetailView,
    ProposalDeleteView,
    ProposalSubmitView,
    RoleRequestCreateView,
)

app_name = "proposals"

urlpatterns = [
    path("", ProposalListView.as_view(), name="list"),
    path("request-role/", RoleRequestCreateView.as_view(), name="request_role"),
    path("new/", ProposalCreateView.as_view(), name="create"),
    path("<int:pk>/", ProposalDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", ProposalUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ProposalDeleteView.as_view(), name="delete"),
    path("<int:pk>/submit/", ProposalSubmitView.as_view(), name="submit"),
]
