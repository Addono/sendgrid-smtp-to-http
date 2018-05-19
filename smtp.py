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
            from_email = Email(self.find_header_value('From'))
            to_email = Email(self.find_header_value('To'))
            subject = self.find_header_value('Subject')
            content = Content(self.find_header_value('Content-Type'), re.match('\n\n([\s\S])*').group(1))
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print str(e)

    def find_header_value(self, header):
        regex = re.match('(\n|^)' + header + ': (\S)*')
        if (header is None):
            print('Could not find header: ' + header)

        return regex.group(1)



def run():
    foo = SendGridHttp(('localhost', 2525), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()