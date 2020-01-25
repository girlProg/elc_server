from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime



VariableAdjustment_CHOOSE=(('Positive','Positive'),('Negative','Negative'))


class ParentModel(models.Model):
    created=models.DateTimeField(auto_now_add=True,null=True)
    modified=models.DateTimeField(auto_now=True,null=True)
    class Meta:
        abstract=True
        ordering = ['-modified']


class SchoolBranch(ParentModel):
    name = models.CharField(default= "", max_length=500, blank=True, null=True)
    address = models.CharField(default= "", max_length=500, blank=True, null=True)
    pensionID = models.CharField(default= "", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class PensionCollector(ParentModel):
    name = models.CharField(default= "", max_length=500, blank=True, null=True)
    address = models.CharField(default= "", max_length=500, blank=True, null=True)
    pensionID = models.CharField(default= "", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Staff(ParentModel):
    name = models.CharField(default= "", max_length=500, blank=True, null=True)
    pension_code = models.CharField(default= "", max_length=500, blank=True, null=True)
    schoolBranch = models.ForeignKey(SchoolBranch, related_name='staff', on_delete=models.CASCADE, blank=True,null=True)
    pension_collector = models.ForeignKey(PensionCollector, related_name='pension_collector', on_delete=models.CASCADE, blank=True,null=True)
    _id = models.CharField(default= "", max_length=500, blank=True, null=True)
    salaryAmount = models.FloatField(default=0, blank=True)
    grossIncome = models.FloatField(default=0, blank=True)
    nhis = models.FloatField(default=0, blank=True)
    allowanceforHeads = models.FloatField(default=0, blank=True)
    isCurrentStaff = models.BooleanField(default=True, null=True, blank=True)
    tax = models.FloatField(default=0, blank=True)
    isAccountsStaff = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name

class Bank(ParentModel):
    name = models.CharField(blank=True,default='', max_length=500)

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
    tax = models.FloatField(default=0, blank=True)
    month = models.CharField(max_length=500, blank=True, null=True, default=str(datetime.now().month))
    year = models.CharField(max_length=500, blank=True, null=True, default=str(datetime.now().year))
    credittobank = models.FloatField(default=0, blank=True)
    salaryAmount = models.FloatField(default=0, blank=True)
    grossIncome = models.FloatField(default=0, blank=True)
    nhis = models.FloatField(default=0, blank=True)
    allowanceforHeads = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.month + ' - '  + self.year + ' ' + self.staff.name


    class Meta:
        unique_together = ("staff", 'month', 'year')


    def addall(self):
        # return 2
        return self.basic.all()[0].amount + self.housing.all()[0].amount +\
               self.transport.all()[0].amount + self.meal.all()[0].amount + \
               self.utility.all()[0].amount + self.entertainment.all()[0].amount +\
               self.dressing.all()[0].amount + self.education.all()[0].amount +\
               self.domestic.all()[0].amount

    def __str__(self):
        return self.staff.name



def save_salary(sender, instance, **kwargs):
    #save the object again incase the salary amount changed this is not best for old payslips before a salary increment. will need to make them immutable
    allowance, created = SBasic.objects.get_or_create(salary=instance)
    allowance.save() if not created else None
    allowance, created = SHousing.objects.get_or_create(salary=instance)
    allowance.save() if not created else None
    allowance, created = STransport.objects.get_or_create(salary=instance)
    allowance.save() if not created else None
    allowance, created = SMeal.objects.get_or_create(salary=instance)
    allowance.save() if not created else None
    allowance, created = SUtility.objects.get_or_create(salary=instance)
    allowance.save() if not created else None
    allowance, created = SEntertainment.objects.get_or_create(salary=instance)
    allowance.save() if not created else None
    allowance, created = SDressing.objects.get_or_create(salary=instance)
    allowance.save() if not created else None
    allowance, created = SEducation.objects.get_or_create(salary=instance)
    allowance.save() if not created else None
    allowance, created = SDomestic.objects.get_or_create(salary=instance)
    allowance.save() if not created else None
    allowance, created = Pension.objects.get_or_create(salary=instance)
    allowance.save() if not created else None

    instance.grossIncome = instance.addall() + instance.allowanceforHeads

    ''' commented out because we are now using variable adjustments instead of predefined
    ones like tahfeez, Quran, school shop etc'''
    post_save.disconnect(save_salary, sender=PaySlip)
    instance.save()
    instance.credittobank = instance
    # Negatives.objects.get_or_create(salary=instance)
    post_save.connect(save_salary, sender=PaySlip)

post_save.connect(save_salary, sender=PaySlip)



class SBasic(ParentModel):
    constant = models.FloatField(default=0.3, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip, null=True, blank=True, related_name='basic', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        #super(self.__class__,self).save(*args,**kwargs)
        self.amount = self.constant * self.salary.salaryAmount
        super(self.__class__,self).save(*args,**kwargs)

    def __str__(self):
        return str(self.amount)



class SHousing(ParentModel):
    constant = models.FloatField(default=0.15, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip, null=True, blank=True, related_name='housing', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.salary.salaryAmount
        super(self.__class__,self).save(*args,**kwargs)


class STransport(ParentModel):
    constant = models.FloatField(default=0.1, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip, null=True, blank=True, related_name='transport', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.salary.salaryAmount
        super(self.__class__,self).save(*args,**kwargs)



class SMeal(ParentModel):
    constant = models.FloatField(default=0.1, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip,null=True, blank=True, related_name='meal', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.salary.salaryAmount
        super(self.__class__,self).save(*args,**kwargs)


class SUtility(ParentModel):
    constant = models.FloatField(default=0.075, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip, null=True, blank=True, related_name='utility', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.salary.salaryAmount
        super(self.__class__,self).save(*args,**kwargs)


class SEntertainment(ParentModel):
    constant = models.FloatField(default=0.05, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip, null=True, blank=True, related_name='entertainment', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.salary.salaryAmount
        super(self.__class__,self).save(*args,**kwargs)



class SDressing(ParentModel):
    constant = models.FloatField(default=0.075, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip, null=True, blank=True, related_name='dressing', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.salary.salaryAmount
        super(self.__class__,self).save(*args,**kwargs)



class SEducation(ParentModel):
    constant = models.FloatField(default=0.1, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip, null=True, blank=True, related_name='education', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.salary.salaryAmount
        super(self.__class__,self).save(*args,**kwargs)



class SDomestic(ParentModel):
    constant = models.FloatField(default=0.05, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip, null=True, blank=True, related_name='domestic', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.amount = self.constant * self.salary.salaryAmount
        super(self.__class__,self).save(*args,**kwargs)





class Pension(ParentModel):
    constant = models.FloatField(default=0.075, blank=True)
    amount = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip,null=True, blank=True, related_name='pension', on_delete=models.CASCADE)

def save_pension(sender, instance, **kwargs):
    post_save.disconnect(save_pension, sender=Pension)
    instance.amount = instance.constant * (instance.salary.basic.all()[0].amount + instance.salary.housing.all()[0].amount + instance.salary.transport.all()[0].amount)
    instance.save()
    post_save.connect(save_pension, sender=Pension)

post_save.connect(save_pension, sender=Pension)

class Negatives(ParentModel):
    neg_schoolshop = models.FloatField(default=0, blank=True)
    neg_schoolfeesadvloan = models.FloatField(default=0, blank=True)
    neg_deduction = models.FloatField(default=0, blank=True)
    neg_feeding = models.FloatField(default=0, blank=True)

    pos_refund = models.FloatField(default=0, blank=True)
    pos_tahfeez = models.FloatField(default=0, blank=True)

    neg_total = models.FloatField(default=0, blank=True)
    pos_total = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip, null=True, blank=True,related_name='negatives', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.neg_total = self.neg_schoolshop + self.neg_schoolfeesadvloan+ self.neg_deduction + self.neg_feeding
        self.pos_total = self.pos_refund + self.pos_tahfeez
        super(self.__class__,self).save(*args,**kwargs)

class Positives(ParentModel):
    refund = models.FloatField(default=0, blank=True)
    tahfeez = models.FloatField(default=0, blank=True)
    total = models.FloatField(default=0, blank=True)
    salary = models.ForeignKey(PaySlip,  null=True, blank=True, related_name='positives', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.total = self.refund + self.tahfeez
        super(self.__class__,self).save(*args,**kwargs)

class VariableAdjustment(ParentModel):
    name = models.CharField(default= "", max_length=500, blank=True, null=True)
    type = models.CharField(default= "", max_length=500, blank=True, null=True, choices=VariableAdjustment_CHOOSE,)
    amount = models.FloatField(default=0, blank=True)
    payslip = models.ForeignKey(PaySlip,  null=True, blank=True, related_name='varadj', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.type

    # def save(self, *args, **kwargs):
    #     self.total = self.refund + self.tahfeez
    #     super(self.__class__,self).save(*args,**kwargs)



def update_salary(sender, instance, **kwargs):
    #TODO: currently does not detect when a partner has not

    x = instance.salary
    # x.credittobank = (x.grossIncome - x.pension.first().amount - x.nhis - x.tax) + instance.pos_total - instance.neg_total
    x.credittobank = (x.grossIncome - x.pension.first().amount - x.nhis - x.tax) + instance.pos_total - instance.neg_total
    post_save.disconnect(save_salary, sender=PaySlip)
    x.save()
    post_save.connect(save_salary, sender=PaySlip)


    # if sender._meta.object_name == 'Positives':
    #     if not x.credittobank:
    #         x.credittobank = (x.grossIncome - x.pension.first().amount - x.nhis - x.tax) + instance.total
    #     else:
    #         if x.credittobank == ((x.grossIncome - x.pension.first().amount - x.nhis - x.tax) + instance.total):
    #             pass #IF THE EXISTING POS/NEG HAS ALREADY BEEN ADDED
    #         else:
    #             x.credittobank = x.credittobank + instance.total
    # else:
    #     if not x.credittobank:
    #         x.credittobank = (x.grossIncome - x.pension.first().amount - x.nhis - x.tax) - instance.total
    #     else:
    #         if x.credittobank == ((x.grossIncome - x.pension.first().amount - x.nhis - x.tax) - instance.total):
    #             pass
    #         else:
    #             x.credittobank = x.credittobank - instance.total
    # instance.staff.save()

    # post_save.disconnect(save_staff, sender=Staff)
    # instance.save()
    # post_save.connect(save_staff, sender=Staff)

# post_save.connect(update_staff, sender=Positives)
post_save.connect(update_salary, sender=Negatives)



def update_payslip(sender, instance, **kwargs):
    payslip = instance.payslip
    if instance.type == 'Positive':
        payslip.credittobank = (payslip.grossIncome - payslip.pension.first().amount - payslip.nhis - payslip.tax) + instance.amount
    else:
        payslip.credittobank = (payslip.grossIncome - payslip.pension.first().amount - payslip.nhis - payslip.tax) - instance.amount
    post_save.disconnect(save_salary, sender=PaySlip)
    payslip.save()
    post_save.connect(save_salary, sender=PaySlip)

post_save.connect(update_payslip, sender=VariableAdjustment)
