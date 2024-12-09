from rest_framework.permissions import BasePermission

class IsOwnerUserOrIsAdminUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user == obj):
            return True
        elif bool(request.user and request.user.is_staff):
            return True
        return False
