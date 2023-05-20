import emails
from credentials import SMTP_Username, SMTP_Password, SMTP_Host, SMTP_Recipient

def send_email(body):

    # Prepare the email
    message = emails.html(
        html="<h1>Daily News</h1>" + body,
        subject="Newsbot Daily",
        mail_from=SMTP_Recipient,
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

if __name__ == '__main__':
    send_email('test')
