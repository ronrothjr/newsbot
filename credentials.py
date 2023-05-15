import emails

ses_user = 'ses-smtp-user.ronrothjr'
SMTP_Username = 'AKIAVRIXCBFHLSNLXD6Y'
SMTP_Password = ''
SMTP_Host = 'email-smtp.us-east-2.amazonaws.com'
SMTP_Recipient = 'ronrothjr@gmail.com'

def send_email(body):

    # Prepare the email
    message = emails.html(
        html="<h1>My message</h1><strong>I've got something to tell you!</strong>",
        subject="A very important message",
        mail_from="MAILER-DAEMON@us-east-2.amazonses.com",
    )

    # Send the email
    r = message.send(
        to=SMTP_Recipient, 
        smtp={
            "host": SMTP_Host,
            "port": 587, 
            "timeout": 5,
            "user": SMTP_Username,
            "password": SMTP_Password,
            "tls": True
        }
    )

    # Check if the email was properly sent
    assert r.status_code == 250

if __name__ == 'main':
    send_email('test')
