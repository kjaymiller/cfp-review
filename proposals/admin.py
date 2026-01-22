from django.contrib import admin
from .models import Tag, Proposal, Review, Selection


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "author__username", "abstract")
    filter_horizontal = ("tags",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("proposal", "reviewer", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("proposal__title", "reviewer__username")


@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    list_display = ("proposal", "organizer", "created_at")
    list_filter = ("created_at",)
    search_fields = ("proposal__title", "organizer__username")
