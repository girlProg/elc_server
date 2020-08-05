from rest_framework import permissions
from .models import Staff


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return Staff.objects.filter(user=request.user).count() > 0


class IsAccountsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        people = Staff.objects.filter(user=request.user)
        return people.count() > 0 and people[0].isAccountsStaff


class IsSchoolAccountActiveForStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        staff = Staff.objects.filter(user=request.user)
        return staff.count() > 0 and staff[0].schoolBranch.school.account.is_active


class IsStaffReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff