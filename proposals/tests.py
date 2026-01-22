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
            score=Review.Score.ACCEPT,
            feedback="Great talk!",
        )
        self.assertEqual(review.score, 1)

    def test_self_review_prevention(self):
        review = Review(
            proposal=self.proposal,
            reviewer=self.author,
            score=Review.Score.ACCEPT,
            feedback="Self praise",
        )
        with self.assertRaises(ValidationError):
            review.save()

    def test_selection_creation(self):
        selection = Selection.objects.create(
            organizer=self.organizer, proposal=self.proposal
        )
        self.assertEqual(selection.proposal, self.proposal)
