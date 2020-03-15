from django.shortcuts import render
import csv
from .models import Staff
from django.http import HttpResponse
from decimal import Decimal
import smtplib
import time
import imaplib
import email


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
            if counter < 10:
                print(counter)
                typ, data = mail.fetch(num, '(RFC822)')
                print
                'Message %s\n%s\n' % (num, data[0][1])
                alert = data[0][1].split(b"\r\nSubject", 1)[1].split(b"\r\nDate:", 1)[0]
                # sender = data[0][1].split(b"ransfer from", 1)[0].split(b"to", 1)[0]
                # return HttpResponse(data[0][1].split(b"\r\nSubject", 1)[1].split(b"to PRINTSTORE", 1)[0])
                if 'Credit' in str(alert) and 'REVERSAL' not in str(alert):
                    msgs.append(str(alert).replace("b': ", '').replace("'", '') + '\r\n')
                    counter = counter + 1
        mail.close()
        mail.logout()
        html = "<html><body> <h1> Print Store Alerts: </h1> <br> <h2> %s. </h2></body></html>" % ' '.join(msgs).replace('\r\n', '<br>')
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
    with open('/home/tymah/webapps/esteem/esteemaccounts/salaryapp/staff.csv') as csv_file:
    # with open('staff.csv') as csv_file:
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
