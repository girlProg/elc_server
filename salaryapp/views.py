from django.shortcuts import render
import csv
from .models import Staff
from django.http import HttpResponse
from decimal import Decimal


def convert_staff(request):
    with open('staff.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        while line_count < 63:
            for row in csv_reader:
                name = row[0].strip()
                salary = Decimal.from_float(float(row[1].strip()))
                allw = Decimal.from_float(float(row[2].strip()))

                Staff.objects.create(name=name, salaryAmount=salary, allowanceforHeads=allw)
                print(f'\t{row[0]} total pay is: {row[1]} allowance for heads: {row[2]} .')
                line_count += 1
        print(f'Processed {line_count} lines.')
        return HttpResponse(line_count)
