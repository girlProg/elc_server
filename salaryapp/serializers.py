from rest_framework import serializers
from . import models
from drf_writable_nested.serializers import WritableNestedModelSerializer


class SBasicSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.SBasic
    fields = ('amount', 'constant',)


class SHousingSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.SHousing
    fields = ('amount', 'constant')

class STransportSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.STransport
    fields = ('amount', 'constant')

class SMealSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.SMeal
    fields = ('amount', 'constant')

class SUtilitySerializer(serializers.ModelSerializer):
  class Meta:
    model = models.SUtility
    fields = ('amount', 'constant')

class SEntertainmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.SEntertainment
    fields = ('amount', 'constant')

class SDressingSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.SDressing
    fields = ('amount', 'constant')

class SEducationSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.SEducation
    fields = ('amount', 'constant')


class SDomesticSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.SDomestic
    fields = ('amount', 'constant')


class PensionSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Pension
    fields = ('amount', 'constant')


class SchoolBranchSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.SchoolBranch
    fields = '__all__'

class PensionCollectorSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.PensionCollector
    fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Bank
    fields = '__all__'

class BankAccountSerializer(WritableNestedModelSerializer):
  bank = BankSerializer()
  class Meta:
    model = models.BankAccount
    fields = '__all__'
    # exclude = ['created', 'modified']


class StaffSerializer(WritableNestedModelSerializer):
  schoolBranch = SchoolBranchSerializer(required=False)
  pension_collector = PensionCollectorSerializer(required=False)
  bankAccount  = BankAccountSerializer(many=True, required=False)
  class Meta:
    model = models.Staff
    fields = '__all__'
    # fields = ('id', 'name', 'allowanceforHeads', 'salaryAmount', 'grossIncome', 'nhis', 'isCurrentStaff')

class PaySlipSerializer(serializers.ModelSerializer):
  basic = SBasicSerializer(required=False, many=True)
  housing = SHousingSerializer(required=False, many=True)
  transport = STransportSerializer(required=False, many=True)
  meal = SMealSerializer(required=False, many=True)
  utility = SUtilitySerializer(required=False, many=True)
  entertainment = SEntertainmentSerializer(required=False, many=True)
  education = SEducationSerializer(required=False, many=True)
  dressing = SDressingSerializer(required=False, many=True)
  domestic = SDomesticSerializer(required=False, many=True)
  pension = PensionSerializer(required=False, many=True)
  staff = StaffSerializer()
  class Meta:
    model = models.PaySlip
    fields = '__all__'
    # fields = ('id','month', 'year', 'date', 'credittobank' ,'tax', 'basic', 'housing', 'transport', 'meal', 'utility', 'entertainment', 'dressing', 'education', 'domestic', 'pension', )


class VariableAdjustmentTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.VariableAdjustmentType
    fields = '__all__'


class VariableAdjustmentSerializer(serializers.ModelSerializer):
  name = VariableAdjustmentTypeSerializer()
  class Meta:
    model = models.VariableAdjustment
    fields = '__all__'
