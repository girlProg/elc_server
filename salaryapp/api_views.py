from . import serializers, models
from rest_framework import viewsets, permissions
from .permissions import *
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class AccountStaffPermissions(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, IsAccountsStaff]
    pass


class StaffViewSet(AccountStaffPermissions):
    serializer_class = serializers.StaffSerializer
    queryset = models.Staff.objects.all()


class PaySlipViewSet(AccountStaffPermissions):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.PaySlipSerializer
    queryset = models.PaySlip.objects.all()
    filter_fields = ('month', 'year', )

    def create(self, request, *args, **kwargs):
        # cannot create payslips via API
        # they are auto generated
        pass


class SBasicViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SBasicSerializer
    queryset = models.SBasic.objects.all()

class SHousingViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SHousingSerializer
    queryset = models.SHousing.objects.all()

class STransportViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.STransportSerializer
    queryset = models.STransport.objects.all()

class SMealViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SMealSerializer
    queryset = models.SMeal.objects.all()

class SUtilityViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SUtilitySerializer
    queryset = models.SUtility.objects.all()


class SEntertainmentViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SEntertainmentSerializer
    queryset = models.SEntertainment.objects.all()

class SDressingViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SDressingSerializer
    queryset = models.SDressing.objects.all()

class SDomesticViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SDomesticSerializer
    queryset = models.SDomestic.objects.all()

class SMedicalViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SMedicalSerializer
    queryset = models.SMedical.objects.all()


class PensionViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.PensionSerializer
    queryset = models.Pension.objects.all()


class PensionCollectorViewSet(AccountStaffPermissions):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.PensionCollectorSerializer
    queryset = models.PensionCollector.objects.all()


class VariableAdjustmentTypeViewSet(AccountStaffPermissions):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.VariableAdjustmentTypeSerializer
    queryset = models.VariableAdjustmentType.objects.all()


class VariableAdjustmentViewSet(AccountStaffPermissions):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.VariableAdjustmentSerializer
    queryset = models.VariableAdjustment.objects.all()
    filter_fields = ('payslip__month', 'payslip__year',)

class BankViewSet(AccountStaffPermissions):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.BankSerializer
    queryset = models.Bank.objects.all()


class BankAccountViewSet(AccountStaffPermissions):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.BankAccountSerializer
    queryset = models.BankAccount.objects.all()


class SchoolBranchViewSet(AccountStaffPermissions):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SchoolBranchSerializer
    queryset = models.SchoolBranch.objects.all()

