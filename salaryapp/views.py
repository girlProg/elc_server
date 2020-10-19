from django.shortcuts import render
import csv
from .models import Staff, PaySlip, SchoolBranch, VariableAdjustment
from django.http import HttpResponse
from decimal import Decimal
import smtplib
import time
import imaplib
import email
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser


ORG_EMAIL   = "@yedi.com.ng"
FROM_EMAIL  = "ps" + ORG_EMAIL
FROM_PWD    = "PSLarafaha"
SMTP_SERVER = "mail.webfaction.com"
SMTP_PORT   = 993




def ps_email(request):
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
        mail.login('psyedi', FROM_PWD)
        mail.select('INBOX')
        msgs = []
        counter = 0
        typ, data = mail.search(None, 'ALL')


        for num in data[0].split()[::-1] :
            if counter < 19:
                print(counter)
                typ, data = mail.fetch(num, '(RFC822)')
                # print ('Message %s\n%s\n' % (num, data[0][1]))
                # alert = data[0][1].split(b"\r\nSubject", 1)[1].split(b"\r\nDate:", 1)[0]
                alert = email.message_from_bytes(data[0][1].split(b"\r\nSubject", 1)[1].split(b"\r\nDate:", 1)[1]).as_string()
                remark = alert.split('Remarks')[1].split('Time of Transaction')[0].strip().replace('=20', '', 20)
                amount = alert.split('Amount')[1].split('Value Date')[0].strip().replace('=20', '', 20)
                date = alert.split('Value Date')[1].split('Remarks')[0].strip().replace('=20', '', 20)



                # with open(data[0][1], 'rb') as fp:
                #     msg = BytesParser(policy=policy.default).parse(fp)

                # Now the header items can be accessed as a dictionary, and any non-ASCII will
                # be converted to unicode:
                #     print('To:', msg['to'])
                #     print('From:', msg['from'])
                #     print('Subject:', msg['subject'])

                # sender = data[0][1].split(b"ransfer from", 1)[0].split(b"to", 1)[0]
                # return HttpResponse(data[0][1].split(b"\r\nSubject", 1)[1].split(b"to PRINTSTORE", 1)[0])
                if 'Credit' in str(alert) and 'REVERSAL' not in str(alert):
                    # msgs.append(str(alert).replace("b': ", '').replace("'", '') + '\r\n')
                    # msgs.append(remark)
                    # msgs.append(amount)
                    msgs.append(f'{date} - ₦{amount} <br> {remark} <br><br>')
                    counter = counter + 1
        mail.close()
        mail.logout()
        # html = "<html><body> <h1> Print Store Alerts: </h1> <br> <h2> %s. </h2></body></html>" % ' '.join(msgs).replace('\r\n', '<br>')
        html = "<html><body> <h1> Print Store Alerts: </h1> <br> <h2> %s. </h2></body></html>" % ' '.join(msgs).replace(':', '')
        return HttpResponse(html)

        # type, data = mail.search(None, 'ALL')
        # # mail_ids = data[0]
        #
        # # id_list = data.split()
        # first_email_id = int(str(data[0])[2])
        # latest_email_id = int(str(data[0])[-2])
        #
        # for i in range(latest_email_id, first_email_id, -1):
        #     typ, data = mail.fetch(i, '(RFC822)')
        #
        #     for response_part in data:
        #         if isinstance(response_part, tuple):
        #             msg = email.message_from_string(response_part[1])
        #             email_subject = msg['subject']
        #             email_from = msg['from']
        #             print('From : ' + email_from + '\n')
        #             print('Subject : ' + email_subject + '\n')
        #             return HttpResponse(email_subject)

    except Exception as e:
        return HttpResponse(e)



def convert_staff(request):
    # with open('/home/tymah/webapps/esteem/esteemaccounts/wuse_staff.csv') as csv_file:
    with open('wuse_staff.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # while line_count < 63:

        for row in csv_reader:
            name = row[0].strip()
            salary = Decimal.from_float(float(row[1].strip()))
            allw = Decimal.from_float(float(row[2].strip()))
            is_pension = row[3].strip()
            tax_due = Decimal.from_float(float(row[4].strip()))
            # school_shop = Decimal.from_float(float(row[5].strip()))
            # fees_saladv_loan = Decimal.from_float(float(row[6].strip()))
            # training = Decimal.from_float(float(row[7].strip()))
            # farm = Decimal.from_float(float(row[8].strip()))
            # feeding = Decimal.from_float(float(row[9].strip()))
            # tahfeez = Decimal.from_float(float(row[10].strip()))
            # tobank = Decimal.from_float(float(row[11].strip()))

            br, ob = SchoolBranch.objects.get_or_create(name="Wuse")

            # chan = str(school_shop) + str(fees_saladv_loan) + str(training)+str(farm)+ str(tax_due)+ str(tahfeez)+ str(feeding)
            pen = False

            if is_pension == 'TRUE':
                pen = True
            else:
                pen = False

            staf = Staff.objects.create(name=name, salaryAmount=salary, allowanceforHeads=allw, is_pensioner=pen, schoolBranch=br)
            payslip = PaySlip.objects.filter(staff=staf)[0]
            # print("-------" + chan)
            # print('matching tax for: ' + staf.name) if str(payslip.tax).split('.')[0] == str(tax_due) else print('mismatch tax for: ' + staf.name + ' - (' + str(payslip.tax).split('.')[0] + ' / '  + str(tax_due) + ' - )' )
            # print('correct alert for: ' + staf.name) if str(payslip.credittobank).split('.')[0] == str(tobank) else print('wrong alert for: ' + staf.name + ' - (' + str(payslip.credittobank).split('.')[0] + ' / '  + str(tobank) + ' - )' )

            line_count += 1
    print(f'Processed {line_count} lines.')
    return HttpResponse(line_count)


def lokogoma_staff(request):
    # with open('/ 3/tymah/webapps/esteem/esteemaccounts/lokogoma_staff.csv') as csv_file:
    with open('lokogoma_staff.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # while line_count < 63:

        for row in csv_reader:
            name = row[0].strip()
            salary = Decimal.from_float(float(row[1].strip()))
            allw = Decimal.from_float(float(row[2].strip()))
            is_pension = row[3].strip()
            tax_due = Decimal.from_float(float(row[4].strip()))
            # school_shop = Decimal.from_float(float(row[5].strip()))
            # fees_saladv_loan = Decimal.from_float(float(row[6].strip()))
            # training = Decimal.from_float(float(row[7].strip()))
            # farm = Decimal.from_float(float(row[8].strip()))
            # feeding = Decimal.from_float(float(row[9].strip()))
            # tahfeez = Decimal.from_float(float(row[10].strip()))
            # tobank = Decimal.from_float(float(row[11].strip()))

            br, ob = SchoolBranch.objects.get_or_create(name="Lokogoma")

            # chan = str(school_shop) + str(fees_saladv_loan) + str(training)+str(farm)+ str(tax_due)+ str(tahfeez)+ str(feeding)
            pen = False

            if is_pension == 'TRUE':
                pen = True
            else:
                pen = False

            staf = Staff.objects.create(name=name, salaryAmount=salary, allowanceforHeads=allw, is_pensioner=pen, schoolBranch=br)
            payslip = PaySlip.objects.filter(staff=staf)[0]
            # print("-------" + chan)
            # print('matching tax for: ' + staf.name) if str(payslip.tax).split('.')[0] == str(tax_due) else print('mismatch tax for: ' + staf.name + ' - (' + str(payslip.tax).split('.')[0] + ' / '  + str(tax_due) + ' - )' )
            # print('correct alert for: ' + staf.name) if str(payslip.credittobank).split('.')[0] == str(tobank) else print('wrong alert for: ' + staf.name + ' - (' + str(payslip.credittobank).split('.')[0] + ' / '  + str(tobank) + ' - )' )

            line_count += 1
    print(f'Processed {line_count} lines.')
    return HttpResponse(line_count)
