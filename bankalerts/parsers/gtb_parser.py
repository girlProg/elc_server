
from django.http import HttpResponse
import imaplib
import email


ORG_EMAIL   = "@yedi.com.ng"
FROM_EMAIL  = "esteem.acct" + ORG_EMAIL
FROM_PWD    = "esteemacct"
SMTP_SERVER = "mail.webfaction.com"
SMTP_PORT   = 993




def gtb_parser(request):
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
