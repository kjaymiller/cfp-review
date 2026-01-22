from django.urls import path
from .views import ProposalListView

app_name = "proposals"

urlpatterns = [
    path("my-proposals/", ProposalListView.as_view(), name="proposal_list"),
    # Placeholder for detail view to avoid template errors if we decide to link it
    # path("<int:pk>/", lambda request, pk: None, name="proposal_detail"),
]
