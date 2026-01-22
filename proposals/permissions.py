from django.contrib.auth import get_user_model

User = get_user_model()


def is_reviewer(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name="Reviewer").exists()


def is_organizer(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name="Organizer").exists()
