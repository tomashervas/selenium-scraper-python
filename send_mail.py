import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

# Configura tus credenciales
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("PASSMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")

cuerpo_correo = """
Hola,

Este es un ejemplo de correo electrónico.

Saludos
"""

em = EmailMessage()

em['From'] = sender_email
em['To'] = receiver_email
em['Subject'] = 'Asunto del correo'
em.set_content(cuerpo_correo)

# Establece una conexión con el servidor SMTP de Gmail
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, em.as_string())
    print(f"Correo electrónico enviado correctamente a {receiver_email}")
except Exception as e:
    print(f"No se pudo enviar el correo: {str(e)}")
    quit()


# Cierra la conexión con el servidor SMTP
server.quit()
