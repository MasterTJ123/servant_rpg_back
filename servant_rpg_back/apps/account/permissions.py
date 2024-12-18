from rest_framework.permissions import BasePermission


class IsOwnerUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            if request.user == obj.user:
                return True
        elif request.user == obj:
            return True
        else:
            return False
