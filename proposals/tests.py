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

        response = self.client.get(reverse("proposals:list"))
        self.assertNotEqual(response.status_code, 200)

    def test_my_proposals_view_lists_own_proposals(self):
        from django.urls import reverse

        self.client.force_login(self.user)
        response = self.client.get(reverse("proposals:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft Proposal")
        self.assertContains(response, "Active Proposal")
        self.assertNotContains(response, "Other Proposal")

    def test_filter_drafts(self):
        from django.urls import reverse

        self.client.force_login(self.user)
        response = self.client.get(reverse("proposals:list") + "?status=draft")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft Proposal")
        self.assertNotContains(response, "Active Proposal")

    def test_filter_review_requested(self):
        from django.urls import reverse

        self.client.force_login(self.user)
        response = self.client.get(
            reverse("proposals:list") + "?status=review_requested"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Draft Proposal")
        self.assertContains(response, "Active Proposal")
        self.assertNotContains(response, "Other Proposal")

    def test_create_proposal(self):
        from django.urls import reverse

        self.client.force_login(self.user)
        url = reverse("proposals:create")
        data = {
            "title": "New Proposal",
            "abstract": "New Abstract",
            "private_notes": "My notes",
            "status": "draft",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("proposals:list"))
        self.assertEqual(Proposal.objects.filter(title="New Proposal").count(), 1)
        proposal = Proposal.objects.get(title="New Proposal")
        self.assertEqual(proposal.author, self.user)

    def test_update_proposal(self):
        from django.urls import reverse

        self.client.force_login(self.user)
        url = reverse("proposals:update", args=[self.p1.pk])
        data = {
            "title": "Updated Title",
            "abstract": "Updated Abstract",
            "status": "review_requested",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("proposals:list"))
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.title, "Updated Title")
        self.assertEqual(self.p1.status, Proposal.Status.REVIEW_REQUESTED)

    def test_update_proposal_permission(self):
        from django.urls import reverse

        # Try to update another user's proposal
        self.client.force_login(self.user)
        url = reverse("proposals:update", args=[self.p3.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_detail_view(self):
        from django.urls import reverse

        self.client.force_login(self.user)
        url = reverse("proposals:detail", args=[self.p1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)
        self.assertContains(response, self.p1.abstract)

    def test_detail_private_notes_visibility(self):
        from django.urls import reverse

        # Add private notes to p1 (owned by user)
        self.p1.private_notes = "Secret Notes"
        self.p1.save()

        # Author viewing own proposal
        self.client.force_login(self.user)
        response = self.client.get(reverse("proposals:detail", args=[self.p1.pk]))
        self.assertContains(response, "Secret Notes")

        # Other user viewing the proposal
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("proposals:detail", args=[self.p1.pk]))
        self.assertNotContains(response, "Secret Notes")
