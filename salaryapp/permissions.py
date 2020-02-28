from rest_framework import permissions
from .models import Staff


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return Staff.objects.filter(user=request.user).count() > 0


class IsAccountsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        people = Staff.objects.filter(user=request.user)
        return people.count() > 0 and people[0].isAccountsStaff


class IsStaffReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff