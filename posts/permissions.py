from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Only allow authors to edit/delete their own posts.
    Read-only for everyone else.
    """
    def has_object_permission(self, request, view, obj):
        # Read-only methods are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.author == request.user
