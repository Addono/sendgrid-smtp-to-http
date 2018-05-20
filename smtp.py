import re
import asyncore
from smtpd import SMTPServer
import sendgrid
from sendgrid.helpers.mail import *
import os
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib

class SendGridHttp(SMTPServer):

    def __init__(self, localaddr, remoteaddr):
        SMTPServer.__init__(self, localaddr, remoteaddr)

        with open('sendgrid_key', 'r+') as content_file:
            data = content_file.read().strip()

            if data is None or data == '':
                print('No API key set in the file: sendgrid_key')
                exit(1)

            print('Sendgrid API key read from storage')
            self.apikey = data

    def process_message(self, peer, mailfrom, rcpttos, data):
        for recipient in rcpttos:
            try:
                subject = self.find_header_value('Subject', data)
                content_type = self.find_header_value('Content-Type', data)

                if content_type == 'text/html':
                    body = re.search(r'(<html [^>]*>(\s\S)</html>)', data).group(1)
                else:
                    body = re.search(r'\n\n([\s\S]*)', data).group(1)

                sg = sendgrid.SendGridAPIClient(apikey=self.apikey)
                data = {
                    "personalizations": [
                        {
                            "to"           : [
                                {
                                    "email": recipient
                                }
                            ],
                            "subject"      : subject
                        },
                    ],
                    "from"            : {
                        "email": mailfrom
                    },
                    "content"         : [
                        {
                            "type" : content_type,
                            "value": body
                        }
                    ],
                }
                try:
                    response = sg.client.mail.send.post(request_body=data)
                except urllib.HTTPError as e:
                    print (e.read())
                    exit()
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print str(e)

    def find_header_value(self, header, data):
        regex = re.compile(header+': ([^\n]*)').search(data)
        if (regex is None):
            print('Could not find header: ' + header)
            return

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