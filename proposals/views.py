from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    ListView,
    DeleteView,
    View,
)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Proposal, RoleRequest
from .forms import ProposalForm, RoleRequestForm
from django.contrib import messages


class RoleRequestCreateView(LoginRequiredMixin, CreateView):
    model = RoleRequest
    form_class = RoleRequestForm
    template_name = "proposals/role_request_form.html"
    success_url = reverse_lazy("proposals:list")

    def form_valid(self, form):
        # Check if user already has a pending request for this role
        existing_request = RoleRequest.objects.filter(
            user=self.request.user,
            role=form.cleaned_data["role"],
            status=RoleRequest.Status.PENDING,
        ).exists()

        if existing_request:
            messages.warning(
                self.request, "You already have a pending request for this role."
            )
            return redirect("proposals:list")

        form.instance.user = self.request.user
        messages.success(self.request, "Role request submitted successfully.")
        return super().form_valid(form)


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


class ProposalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Proposal
    template_name = "proposals/proposal_confirm_delete.html"
    success_url = reverse_lazy("proposals:list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ProposalSubmitView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        proposal = get_object_or_404(Proposal, pk=pk)
        if proposal.status == Proposal.Status.DRAFT:
            proposal.status = Proposal.Status.REVIEW_REQUESTED
            proposal.save()
        return redirect("proposals:detail", pk=pk)

    def test_func(self):
        proposal = get_object_or_404(Proposal, pk=self.kwargs["pk"])
        return proposal.author == self.request.user
