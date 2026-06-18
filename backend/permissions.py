from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.allowed_roles

class IsAdmin(HasRole):
    allowed_roles = ['ADMIN']

class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'ADMIN' or obj.id == request.user.id