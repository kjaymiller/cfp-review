from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Proposal(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        REVIEW_REQUESTED = "review_requested", _("Review Requested")
        ARCHIVED = "archived", _("Archived")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="proposals"
    )
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    private_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    class Score(models.IntegerChoices):
        DISLIKE = -1, _("Dislike")
        NEUTRAL = 0, _("Neutral")
        LIKE = 1, _("Like")

    proposal = models.ForeignKey(
        Proposal, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.IntegerField(choices=Score.choices)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure the proposal exists before checking author
        if hasattr(self, "proposal") and hasattr(self, "reviewer"):
            if self.reviewer == self.proposal.author:
                raise ValidationError(_("You cannot review your own proposal."))

    def save(self, *args, **kwargs):
        # We need to handle the case where self.proposal_id is set but self.proposal is not cached
        # clean() relies on self.proposal.author which triggers a DB hit
        # This is fine for now as per requirements
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review for {self.proposal.title} by {self.reviewer}"


class Selection(models.Model):
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="selections"
    )
    proposal = models.ForeignKey(
        Proposal, on_delete=models.CASCADE, related_name="selections"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Selection: {self.proposal.title}"
