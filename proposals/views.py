from neapolitan.views import CRUDView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Proposal


class ProposalView(LoginRequiredMixin, CRUDView):
    model = Proposal
    fields = ["title", "abstract", "status", "tags"]

    def get_queryset(self):
        queryset = Proposal.objects.filter(author=self.request.user)
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by("-updated_at")
