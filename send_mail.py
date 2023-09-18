import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

   
def send_mail(sender, password, receiver, subject, body):
    """
    Sends an email using the provided sender, password, receiver, subject, and body.
    
    Args:
        sender (str): The email address of the sender.
        password (str): The password associated with the sender's email address.
        receiver (str): The email address of the receiver.
        subject (str): The subject line of the email.
        body (str): The body of the email.
    """ 
    sender_email = sender
    sender_password = password
    receiver_email = receiver

    mail_body = body

    em = MIMEMultipart()

    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.attach(MIMEText(mail_body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, em.as_string())
        print(f"Correo electrónico enviado correctamente a {receiver_email}")
    except Exception as e:
        print(f"No se pudo enviar el correo: {str(e)}")
        quit()

    server.quit()
