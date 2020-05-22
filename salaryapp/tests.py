
# YediTech
# girlProg
# 2020

from django.test import TestCase
from .models import Staff, PaySlip, PensionCollector, Bank
from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class APIPOSTRequestsCreationTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        data = {'name': 'DabApps'}
        response = self.client.post('/api/staff/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Staff.objects.count(), 1)
        self.assertEqual(PaySlip.objects.count(), 2)
        self.assertEqual(Staff.objects.get().name, 'DabApps')

    def test_create_pfa(self):
        data = {'name': 'Premium Pensions'}
        response = self.client.post('/api/pfas/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PensionCollector.objects.count(), 1)
        self.assertEqual(PensionCollector.objects.get().name, 'Premium Pensions')

    def test_create_bank(self):
        data = {'name': 'GTBank'}
        response = self.client.post('/api/bank/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bank.objects.count(), 1)
        self.assertEqual(Bank.objects.get().name, 'GTBank')

    def test_create_varadj(self):
        data = {'name': 'GTBank'}
        response = self.client.post('/api/bank/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bank.objects.count(), 1)
        self.assertEqual(Bank.objects.get().name, 'GTBank')



class NewStaffTestCase(TestCase):
    def setUp(self):
        Staff.objects.create(name="TestStaff", salaryAmount=Decimal.from_float(10000))

    def test_autogen_payslip(self):
        """Payslip tests"""
        # print('Testing autogen payslip')
        staff = Staff.objects.get(name="TestStaff")
        payslip = PaySlip.objects.get(staff=staff, month=datetime.now().month)
        self.assertEqual(payslip.year, str(datetime.now().year))
        self.assertEqual(payslip.basic.all()[0].amount, 3000)
        self.assertEqual(payslip.housing.all()[0].amount, 1500)
        self.assertEqual(payslip.transport.all()[0].amount, 1000)
        self.assertEqual(payslip.meal.all()[0].amount, 1000)
        self.assertEqual(payslip.utility.all()[0].amount, 1000)
        self.assertEqual(payslip.medical.all()[0].amount, 500)
        self.assertEqual(payslip.dressing.all()[0].amount, 1000)
        self.assertEqual(payslip.education.all()[0].amount, 1000)
        self.assertEqual(payslip.pension.all()[0].amount, 412.50)
        self.assertEqual(payslip.salaryAmount, 10000)
        self.assertEqual(payslip.grossIncome, 10000)
        self.assertEqual(payslip.nhis, 0)
        self.assertEqual(payslip.tax, 100)
        self.assertEqual(payslip.allowanceforHeads, 0)
        self.assertEqual(payslip.credittobank, 9487.50)
        # print('Passed')


class EditStaffTestCase(TestCase):
    def setUp(self):
        Staff.objects.create(name="TestStaff", salaryAmount=Decimal.from_float(10000))
        sta = Staff.objects.get(name="TestStaff")
        sta.salaryAmount = 20000
        sta.save()

    def test_edit_payslip(self):
        """Payslip tests"""
        # print('Testing editing payslip')
        staff = Staff.objects.get(name="TestStaff")
        payslip = PaySlip.objects.get(staff=staff, month=datetime.now().month)
        self.assertEqual(payslip.year, str(datetime.now().year))
        self.assertEqual(payslip.basic.all()[0].amount, 6000)
        self.assertEqual(payslip.housing.all()[0].amount, 3000)
        self.assertEqual(payslip.transport.all()[0].amount, 2000)
        self.assertEqual(payslip.meal.all()[0].amount, 2000)
        self.assertEqual(payslip.utility.all()[0].amount, 2000)
        self.assertEqual(payslip.dressing.all()[0].amount, 2000)
        self.assertEqual(payslip.education.all()[0].amount, 2000)
        self.assertEqual(payslip.pension.all()[0].amount, 825)
        self.assertEqual(payslip.salaryAmount, 20000)
        self.assertEqual(payslip.grossIncome, 20000)
        self.assertEqual(payslip.nhis, 0)
        self.assertEqual(payslip.tax, 200)
        self.assertEqual(payslip.allowanceforHeads, 0)
        self.assertEqual(payslip.credittobank, 18975)
        # print('Passed')

    def test_second_edit_payslip(self):
        """Payslip tests"""
        # print('Testing editing payslip')
        staff = Staff.objects.get(name="TestStaff")
        date = datetime.now() + relativedelta(months=1)
        payslip = PaySlip.objects.get(staff=staff, month=date.month)
        self.assertEqual(payslip.year, str(date.year))
        self.assertEqual(payslip.basic.all()[0].amount, 6000)
        self.assertEqual(payslip.housing.all()[0].amount, 3000)
        self.assertEqual(payslip.transport.all()[0].amount, 2000)
        self.assertEqual(payslip.meal.all()[0].amount, 2000)
        self.assertEqual(payslip.utility.all()[0].amount, 2000)
        self.assertEqual(payslip.dressing.all()[0].amount, 2000)
        self.assertEqual(payslip.education.all()[0].amount, 2000)
        self.assertEqual(payslip.pension.all()[0].amount, 825)
        self.assertEqual(payslip.salaryAmount, 20000)
        self.assertEqual(payslip.grossIncome, 20000)
        self.assertEqual(payslip.nhis, 0)
        self.assertEqual(payslip.tax, 200)
        self.assertEqual(payslip.allowanceforHeads, 0)
        self.assertEqual(payslip.credittobank, 18975)
        # print('Passed')

