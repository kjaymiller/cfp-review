from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Tag, Proposal, Review, Selection

User = get_user_model()


class ProposalModelTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="password")
        self.reviewer = User.objects.create_user(
            username="reviewer", password="password"
        )
        self.organizer = User.objects.create_user(
            username="organizer", password="password"
        )
        self.tag = Tag.objects.create(name="Python")
        self.proposal = Proposal.objects.create(
            author=self.author,
            title="My Talk",
            abstract="Abstract content",
            status=Proposal.Status.REVIEW_REQUESTED,
        )
        self.proposal.tags.add(self.tag)

    def test_proposal_creation(self):
        self.assertEqual(str(self.proposal), "My Talk")
        self.assertEqual(self.proposal.tags.count(), 1)
        self.assertEqual(self.proposal.status, Proposal.Status.REVIEW_REQUESTED)

    def test_review_creation(self):
        review = Review.objects.create(
            proposal=self.proposal,
            reviewer=self.reviewer,
            score=Review.Score.LIKE,
            feedback="Great talk!",
        )
        self.assertEqual(review.score, 1)

    def test_self_review_prevention(self):
        review = Review(
            proposal=self.proposal,
            reviewer=self.author,
            score=Review.Score.LIKE,
            feedback="Self praise",
        )
        with self.assertRaises(ValidationError):
            review.save()

    def test_selection_creation(self):
        selection = Selection.objects.create(
            organizer=self.organizer, proposal=self.proposal
        )
        self.assertEqual(selection.proposal, self.proposal)


class ProposalViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="speaker", password="password")
        self.other_user = User.objects.create_user(
            username="other", password="password"
        )

        self.p1 = Proposal.objects.create(
            author=self.user,
            title="Draft Proposal",
            status=Proposal.Status.DRAFT,
            abstract="Abstract 1",
        )
        self.p2 = Proposal.objects.create(
            author=self.user,
            title="Active Proposal",
            status=Proposal.Status.REVIEW_REQUESTED,
            abstract="Abstract 2",
        )
        self.p3 = Proposal.objects.create(
            author=self.other_user,
            title="Other Proposal",
            status=Proposal.Status.DRAFT,
            abstract="Abstract 3",
        )

    def test_my_proposals_view_requires_login(self):
        from django.urls import reverse

        response = self.client.get(reverse("proposals:proposal-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_my_proposals_view_lists_own_proposals(self):
        from django.urls import reverse

        self.client.force_login(self.user)
        response = self.client.get(reverse("proposals:proposal-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft Proposal")
        self.assertContains(response, "Active Proposal")
        self.assertNotContains(response, "Other Proposal")

    def test_filter_drafts(self):
        from django.urls import reverse

        self.client.force_login(self.user)
        response = self.client.get(reverse("proposals:proposal-list") + "?status=draft")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft Proposal")
        self.assertNotContains(response, "Active Proposal")

    def test_filter_review_requested(self):
        from django.urls import reverse

        self.client.force_login(self.user)
        response = self.client.get(
            reverse("proposals:proposal-list") + "?status=review_requested"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Draft Proposal")
        self.assertContains(response, "Active Proposal")
        self.assertNotContains(response, "Other Proposal")
