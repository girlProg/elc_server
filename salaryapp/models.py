from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime
from .taxCalculator import calculate_monthly_tax
from dateutil.relativedelta import relativedelta
from decimal import Decimal

VariableAdjustment_CHOOSE = (('Positive', 'Positive'), ('Negative', 'Negative'))


class ParentModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-modified']

class Profile(User, ParentModel):
    name = models.CharField(default="", max_length=500, blank=True, null=True)
    pass


class School(ParentModel):
    name = models.CharField(default="", max_length=500, blank=True, null=True)
    address = models.CharField(default="", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class SchoolBranch(ParentModel):
    name = models.CharField(default="", max_length=500, blank=True, null=True)
    school = models.ForeignKey(School, related_name='schoolbranch', on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(default="", max_length=500, blank=True, null=True)
    pensionID = models.CharField(default="", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class PensionCollector(ParentModel):
    name = models.CharField(default="", max_length=500, blank=True, null=True)
    address = models.CharField(default="", max_length=500, blank=True, null=True)
    pensionID = models.CharField(default="", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Staff(ParentModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff', null=True, blank=True)
    name = models.CharField(default="", max_length=500, blank=True, null=True)
    # pension_code = models.CharField(default="", max_length=500, blank=True, null=True)
    schoolBranch = models.ForeignKey(SchoolBranch, related_name='staff', on_delete=models.CASCADE, blank=True,
                                     null=True)
    pension_collector = models.ForeignKey(PensionCollector, related_name='staff', on_delete=models.CASCADE, blank=True,
                                          null=True)
    _id = models.CharField(default="", max_length=500, blank=True, null=True)
    salaryAmount = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    grossIncome = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    nhis = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    allowanceforHeads = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    isCurrentStaff = models.BooleanField(default=True, null=True, blank=True)
    tax = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    isAccountsStaff = models.BooleanField(default=False, blank=True, null=True)
    is_pensioner = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Bank(ParentModel):
    name = models.CharField(blank=True, default='', max_length=500)

    def __str__(self):
        return self.name


class BankAccount(ParentModel):
    number = models.CharField(blank=True, max_length=11, null=True)
    # manyt = models.ForeignKey(Bank,default='', null=True, blank=True, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, default='', on_delete=models.CASCADE, related_name='bankAccount')
    bank = models.ForeignKey(Bank, default='', on_delete=models.CASCADE, related_name='bankAccount')

    def __str__(self):
        return self.staff.name + ' - ' + self.bank.name


class PaySlip(ParentModel):
    staff = models.ForeignKey(Staff, related_name='payslip', on_delete=models.CASCADE)
    tax = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    month = models.CharField(max_length=500, blank=True, null=True, default=str(datetime.now().month))
    year = models.CharField(max_length=500, blank=True, null=True, default=str(datetime.now().year))
    credittobank = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    salaryAmount = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    grossIncome = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    nhis = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    allowanceforHeads = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.month + ' - ' + self.year + ' ' + self.staff.name

    class Meta:
        unique_together = ("staff", 'month', 'year')

    def addall(self):
        # return 2
        return self.basic.all()[0].amount + self.housing.all()[0].amount + \
               self.transport.all()[0].amount + self.meal.all()[0].amount + \
               self.utility.all()[0].amount +  \
               self.dressing.all()[0].amount + self.education.all()[0].amount + \
               self.medical.all()[0].amount

    def __str__(self):
        return self.staff.name


def save_payslip(sender, instance, **kwargs):
    # save the object again incase the salary amount changed this is not best for old payslips before a salary increment. will need to make them immutable

    # if not instance.salaryAmount:
    # if len(PaySlip.objects.filter(month=instance.month, year=instance.year, staff=instance.staff)) > 0:
    instance.salaryAmount = instance.staff.salaryAmount
    instance.tax = instance.staff.tax
    instance.nhis = instance.staff.nhis
    instance.allowanceforHeads = instance.staff.allowanceforHeads
    post_save.disconnect(save_payslip, sender=PaySlip)
    instance.save()
    post_save.connect(save_payslip, sender=PaySlip)

    allowance, created = SBasic.objects.get_or_create(payslip=instance)
    allowance.save() if not created else None
    allowance, created = SHousing.objects.get_or_create(payslip=instance)
    allowance.save() if not created else None
    allowance, created = STransport.objects.get_or_create(payslip=instance)
    allowance.save() if not created else None
    allowance, created = SMeal.objects.get_or_create(payslip=instance)
    allowance.save() if not created else None
    allowance, created = SUtility.objects.get_or_create(payslip=instance)
    allowance.save() if not created else None
    allowance, created = SMedical.objects.get_or_create(payslip=instance)
    allowance.save() if not created else None
    allowance, created = SDressing.objects.get_or_create(payslip=instance)
    allowance.save() if not created else None
    allowance, created = SEducation.objects.get_or_create(payslip=instance)
    allowance.save() if not created else None
    allowance, created = Pension.objects.get_or_create(payslip=instance)
    allowance.save() if not created else None

    instance.grossIncome = instance.addall() + instance.allowanceforHeads

    ''' commented out because we are now using variable adjustments instead of predefined
    ones like tahfeez, Quran, school shop etc'''
    post_save.disconnect(save_payslip, sender=PaySlip)
    if instance.staff.is_pensioner:
        tax = calculate_monthly_tax(instance.grossIncome, 200000, 20, instance.pension.all()[0].amount, instance.nhis)
    else:
        tax = 0
    # print(tax)
    instance.tax = tax

    post_save.disconnect(create_payslip, sender=Staff)
    instance.staff.tax = tax
    instance.save()
    post_save.connect(create_payslip, sender=Staff)

    # add all var adjs to payslip
    total = 0
    for adj in instance.varadj.all():
        if adj.type == 'Positive':
            total += adj.amount
        else:
            total += -adj.amount
    instance.credittobank = instance.grossIncome - instance.pension.all()[0].amount - instance.nhis - instance.tax + total
    # print(instance.tax)
    # print(instance.credittobank)
    instance.save()

    # Negatives.objects.get_or_create(salary=instance)
    post_save.connect(save_payslip, sender=PaySlip)


def create_payslip(sender, instance, **kwargs):
    # save the object again in case the salary amount
    # this triggers a recalculation of all values within the payslips

    payslip, created = PaySlip.objects.get_or_create(
        month=str(datetime.now().month),
        year=str(datetime.now().year),
        staff=instance
    )

    # create next months payslip
    date_after_month = datetime.today() + relativedelta(months=1)
    payslip2, created2 = PaySlip.objects.get_or_create(
        month=str(date_after_month.month),
        year=str(date_after_month.year),
        staff=instance
    )

    if not created:
        payslip.salaryAmount = instance.salaryAmount
        payslip.nhis = instance.nhis
        payslip.allowanceforHeads = instance.allowanceforHeads
        payslip.tax = instance.tax
        payslip.save()

    if not created2:
        payslip2.salaryAmount = instance.salaryAmount
        payslip2.nhis = instance.nhis
        payslip2.allowanceforHeads = instance.allowanceforHeads
        payslip2.tax = instance.tax
        payslip2.save()


post_save.connect(save_payslip, sender=PaySlip)
post_save.connect(create_payslip, sender=Staff)

''' 
when saving a staff object for the first time, 
    * a payslip is auto generated after saving the staff
    
when saving an existing staff
    * the payslip needs to be updated to have the new staff values

'''


class SBasic(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.3), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='basic', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # super(self.__class__,self).save(*args,**kwargs)
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.amount)


class SHousing(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.15), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='housing', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)


class STransport(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.1), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='transport', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)


class SMeal(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.1), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='meal', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)


class SUtility(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.1), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='utility', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)

# to be swapped with medical
class SEntertainment(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.05), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='entertainment', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)


class SMedical(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.05), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='medical', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)


class SDressing(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.1), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='dressing', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)


class SEducation(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.1), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='education', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)

# TODO: remove all references to domestic
class SDomestic(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.05), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='domestic', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.payslip.salaryAmount
        super(self.__class__, self).save(*args, **kwargs)


class Pension(ParentModel):
    constant = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal.from_float(0.075), blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='pension', on_delete=models.CASCADE)


def save_pension(sender, instance, **kwargs):
    post_save.disconnect(save_pension, sender=Pension)
    if instance.payslip.staff.is_pensioner:
        instance.amount = instance.constant * (
                    instance.payslip.basic.all()[0].amount + instance.payslip.housing.all()[0].amount +
                    instance.payslip.transport.all()[0].amount)
    else:
        instance.amount = 0
    instance.save()
    post_save.connect(save_pension, sender=Pension)


post_save.connect(save_pension, sender=Pension)


class VariableAdjustmentType(ParentModel):
    name = models.CharField(default="", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

class VariableAdjustment(ParentModel):
    name = models.ForeignKey(VariableAdjustmentType, null=True, blank=True, related_name='varadj', on_delete=models.CASCADE)
    type = models.CharField(default="", max_length=500, blank=True, null=True, choices=VariableAdjustment_CHOOSE, )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    payslip = models.ForeignKey(PaySlip, null=True, blank=True, related_name='varadj', on_delete=models.CASCADE)

    def __str__(self):
        return self.name.name + ' ' + self.type

    # def save(self, *args, **kwargs):
    #     self.total = self.refund + self.tahfeez
    #     super(self.__class__,self).save(*args,**kwargs)


def update_payslip(sender, instance, **kwargs):
    total = 0
    for adj in instance.payslip.varadj.all():
        if adj.type == 'Positive':
            total += adj.amount
        else:
            total += -adj.amount
    instance.payslip.credittobank = instance.payslip.grossIncome - instance.payslip.pension.all()[0].amount - instance.payslip.nhis - instance.payslip.tax + total
    # print(instance.tax)
    # print(instance.credittobank)
    post_save.disconnect(save_payslip, sender=PaySlip)
    instance.payslip.save()
    post_save.connect(save_payslip, sender=PaySlip)





post_save.connect(update_payslip, sender=VariableAdjustment)
# post_save.connect(update_payslip_for_payslip_save, sender=PaySlip)

