from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Proposal
from .forms import ProposalForm


class ProposalListView(LoginRequiredMixin, ListView):
    model = Proposal
    context_object_name = "proposals"
    template_name = "proposals/proposal_list.html"

    def get_queryset(self):
        queryset = Proposal.objects.filter(author=self.request.user)
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by("-updated_at")


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = "proposals/proposal_form.html"
    success_url = reverse_lazy("proposals:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProposalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Proposal
    form_class = ProposalForm
    template_name = "proposals/proposal_form.html"
    success_url = reverse_lazy("proposals:list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ProposalDetailView(LoginRequiredMixin, DetailView):
    model = Proposal
    template_name = "proposals/proposal_detail.html"
    context_object_name = "proposal"
