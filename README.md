# Sendgri SMTP to HTTP
A local SMTP server which uses the HTTPv3 API of SendGrid to deliver emails.

This project is developed to offer a solution when Gitlabs outgoing SMTP traffic gets blocked by a firewall. Other usages have not been tested but in theory should they work just fine.

## How to install & use
1. Install the SendGrid python library:
```pip install sendgrid```
2. Add your SendGrid API key to the file `sendgrid_key`
3. Configure your applications to use an SMTP server on `localhost` port `2525`
4. Start the script with `python smtp.py`
