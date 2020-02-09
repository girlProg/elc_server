from decimal import Decimal


# crf - consolidated relief fees
# pa - percentage of annual
# ca - consolidated allowance



def calculate_monthly_tax(monthly_gross, crf, pa, monthly_pension, nhis):
    one_year = 12

    gross_annual = monthly_gross * one_year
    pension_annual = monthly_pension * one_year
    percent_of_annual_gross = Decimal.from_float(pa/100) * gross_annual

    if nhis == 0:
        # 1500 is used as the dummy nhis to help reduce tax amount
        nhis_annual = 1500 * one_year
    else:
        nhis_annual = nhis * one_year

    ca = crf + percent_of_annual_gross + pension_annual + nhis_annual

    taxable_income = gross_annual - ca

    # if earning less than 300k
    if taxable_income < 300000:
        return (gross_annual * Decimal.from_float(1/100) ) / 12




    first_balance = taxable_income - 300000
    first_tax_constant_300 = Decimal.from_float(300000 * (7 / 100))
    second_balance = taxable_income - 600000
    second_tax_constant_300 = Decimal.from_float(300000 * (11 / 100))
    third_balance = taxable_income - 1100000
    third_tax_constant_500 = Decimal.from_float(500000 * (15 / 100))
    fourth_balance = taxable_income - 1600000
    fourth_tax_constant_500 = 500000 * (21 / 100)
    fifth_balance = taxable_income - 3100000
    fifth_tax_constant_500 = 1600000 * (21 / 100)

    if 300000 < taxable_income < 600000:
        second_tranche_calc = Decimal.from_float(11 / 100) * (taxable_income - 300000)
        return (first_tax_constant_300 + second_tranche_calc)/Decimal.from_float(12)

    if 300000 < taxable_income < 1100000:
        third_tranche_calc = Decimal.from_float(15 / 100) * (taxable_income - 500000)
        return (first_tax_constant_300 + second_tax_constant_300 + third_tranche_calc) / Decimal.from_float(12)

    if 300000 < taxable_income < 1600000:
        fourth_tranche_calc = Decimal.from_float(19 / 100) * (taxable_income - 500000)
        return (first_tax_constant_300 + second_tax_constant_300 + third_tax_constant_500 +fourth_tranche_calc) / Decimal.from_float(12)

    if 300000 < taxable_income < 3200000:
        fourth_tranche_calc = Decimal.from_float(19 / 100) * (taxable_income - 500000)
        return (first_tax_constant_300 + second_tax_constant_300 + third_tax_constant_500 +fourth_tranche_calc) / Decimal.from_float(12)







