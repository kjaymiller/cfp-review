from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Proposal


class ProposalListView(LoginRequiredMixin, ListView):
    model = Proposal
    template_name = "proposals/proposal_list.html"
    context_object_name = "proposals"

    def get_queryset(self):
        queryset = Proposal.objects.filter(author=self.request.user)
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by("-updated_at")
