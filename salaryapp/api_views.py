from . import serializers, models
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class StaffViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.StaffSerializer
    queryset = models.Staff.objects.all()


    # def update(self, request, *args, **kwargs):
    #     print(request.method)
    #     try:
    #         if len(list(request.data)) > 1:
    #             obj = models.Staff.objects.get(id=request.data['id'])
    #             inst = serializers.StaffSerializer(data=request.data)
    #             if inst.is_valid():
    #                 inst.save()
    #             print(obj)
    #             print(inst)
    #             return Response(inst)
    #     except Exception as e:
    #         # rollbar.report_exc_info(extra_data={'error': e, 'message': e, 'user': request.data })
    #         return Response({'error': 'Error changing password: ' + str(e)}, status=409)



class PaySlipViewSet(viewsets.ModelViewSet):
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


class PensionCollectorViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.PensionCollectorSerializer
    queryset = models.PensionCollector.objects.all()


class VariableAdjustmentTypeViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.VariableAdjustmentTypeSerializer
    queryset = models.VariableAdjustmentType.objects.all()


class VariableAdjustmentViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.VariableAdjustmentSerializer
    queryset = models.VariableAdjustment.objects.all()
    filter_fields = ('payslip__month', 'payslip__year',)

class BankViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.BankSerializer
    queryset = models.Bank.objects.all()


class BankAccountViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.BankAccountSerializer
    queryset = models.BankAccount.objects.all()


class SchoolBranchViewSet(viewsets.ModelViewSet):
    # permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = serializers.SchoolBranchSerializer
    queryset = models.SchoolBranch.objects.all()

