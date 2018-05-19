import re
import asyncore
from smtpd import SMTPServer
import sendgrid
import os
from sendgrid.helpers.mail import *

class SendGridHttp(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        try:
            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email(self.find_header_value('From', data))
            to_email = Email(self.find_header_value('To', data))
            subject = self.find_header_value('Subject', data)
            content = Content(self.find_header_value('Content-Type', data), re.match('\r?\n\r?\n([\s\S])*', data).group(1))
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print str(e)

    def find_header_value(self, header, data):
        regex = re.match('(\n|^)' + header + ': (\S)*', data)
        if (regex is None):
            print('Could not find header: ' + header)

        return regex.group(1)



def run():
    print('Starting SMTP server')
    SendGridHttp(('localhost', 2525), None)
    print('SMTP server started')
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()