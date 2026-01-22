from django.contrib import admin
from .models import Tag, Proposal, Review, Selection, RoleRequest


@admin.register(RoleRequest)
class RoleRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "status", "created_at")
    list_filter = ("status", "role", "created_at")
    search_fields = ("user__username", "user__email")
    actions = ["approve_requests", "reject_requests"]

    @admin.action(description="Approve selected requests")
    def approve_requests(self, request, queryset):
        # We need to call save() on each instance to trigger the group assignment logic
        # queryset.update() does NOT call save() methods
        for req in queryset:
            req.status = RoleRequest.Status.APPROVED
            req.save()
        self.message_user(request, f"{queryset.count()} requests marked as approved.")

    @admin.action(description="Reject selected requests")
    def reject_requests(self, request, queryset):
        queryset.update(status=RoleRequest.Status.REJECTED)
        self.message_user(request, f"{queryset.count()} requests marked as rejected.")


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
