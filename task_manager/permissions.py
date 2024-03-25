from rest_framework import permissions


class AdminModelPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_staff and (request.method == "DELETE"):
            return False

        return True
