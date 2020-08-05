from . import serializers, models
from rest_framework import viewsets, permissions
from .permissions import *
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal


class AccountStaffPermissions(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, IsAccountsStaff, IsSchoolAccountActiveForStaff]
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


class GenerateCurrentMonthPayslipsViewSet(viewsets.ViewSet):

    def list(self, request):
        if len(models.PaySlip.objects.filter(month=datetime.today().month,year=datetime.today().year)) < 1:
            for staff in models.Staff.objects.all():
                if staff.isCurrentStaff:
                    models.PaySlip.objects.get_or_create(
                        month=str(datetime.today().month),
                        year=str(datetime.today().year),
                        staff=staff
                    )
        return Response('current month updated', status=200)


class GenerateNextMonthPayslipsViewSet(viewsets.ViewSet):

    def list(self, request):
        date_after_month = datetime.today() + relativedelta(months=1)
        if len(models.PaySlip.objects.filter(month=date_after_month.month, year=date_after_month.year)) < 1:
            for staff in models.Staff.objects.all():
                if staff.isCurrentStaff:
                    date_after_month = datetime.today() + relativedelta(months=1)
                    models.PaySlip.objects.get_or_create(
                        month=str(date_after_month.month),
                        year=str(date_after_month.year),
                        staff=staff
                    )
        return Response('next month generated', status=200)


class AdjustAllStaffViewSet(viewsets.ViewSet):

    def list(self, request):
        amount = 0
        percent = 0
        type = 0
        month=0

        if 'amount' in request.query_params.keys():
            amount = request.query_params['amount']

        if 'percent' in request.query_params.keys():
            percent = request.query_params['percent']

        if 'type' in request.query_params.keys():
            type = request.query_params['type']

        if 'month' in request.query_params.keys():
            month = request.query_params['month']

        payslips = models.PaySlip.objects.filter(month=month, year=datetime.now().year)
        print(len(payslips))
        varadj_type = models.VariableAdjustmentType.objects.get_or_create(name='Cummulative')[0]

        for payslip in payslips:
            if amount:
                models.VariableAdjustment.objects.get_or_create(name=varadj_type, type=type, amount=amount, payslip=payslip)
            if percent:
                varadj = models.VariableAdjustment.objects.get_or_create(name=varadj_type,
                                                                         type=type,
                                                                         amount=payslip.salaryAmount * Decimal.from_float(int(percent)/100),
                                                                         payslip=payslip)[0]
                payslip.save()
                varadj.save()

        return Response('adjustments added', status=200)
