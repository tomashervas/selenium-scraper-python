import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

   
def send_mail(sender, password, receiver, subject, product_name = "", product_img = "", product_price = 0, product_url = "", product_names = [], products_file_names = [], weekly=False):
    """
    Sends an email using the provided sender, password, receiver, subject, and body.
    
    Args:
        sender (str): The email address of the sender.
        password (str): The password associated with the sender's email address.
        receiver (str): The email address of the receiver.
        subject (str): The subject line of the email.
        product_name (str, optional): The name of the product.
        product_img (str, optional): The URL of the product's image.
        product_price (float, optional): The price of the product.
        product_url (str, optional): The URL of the product.
        product_names (str[], optional): List of product_names.
        products_file_names (str[] , optional): List of product_file_names.
        weekly (bool, optional): Whether to be a weekly email or not. Defaults to False.
        
    """ 


    sender_email = sender
    sender_password = password
    receiver_email = receiver

    em = MIMEMultipart()

    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject

    if weekly:
        mail_body = f"""
                        <html>
                            <body style="margin:0;padding:0;">
                                <p style="font-size: large;">Esta es la evolución de los precios de tus productos:</p>"""
                                

        # img_files = [f for f in os.listdir("images") if os.path.isfile(os.path.join("images", f))]
        # img_files.sort()
        img_files = products_file_names

        for img_file in img_files:
            with open(f'images/{img_file}', 'rb') as file:
                img_data = file.read()
            img_chart = MIMEImage(img_data, name=img_file)
            img_chart.add_header('Content-ID', f'<{img_file}>')
            mail_body += f"""
                            <h2 style="font-weight: bold;">{product_names[img_files.index(img_file)]}</h2>
                            <img src="cid:{img_file}"><br>"""
            
            em.attach(img_chart)

        mail_body += """     
                            </body>
                        </html>
                    """
    else:
        mail_body = f"""
                        <html>
                            <body style="margin:0;padding:0;">
                                <p style="font-size: large;">El precio del producto</p>
                                <h1 style="font-weight: bold;">{product_name}</h1>
                                <img src="{product_img}" alt="" style="width: 40%; margin: 16px 30%;">
                                <p style="font-size: large;">ha bajado a: </p>
                                <h1 style="color: crimson; text-align: center;">{product_price}€</h1>
                                <br>
                                <p style="font-size: large; text-align: right; margin-top: 16px;"><a href="{product_url}" style="text-decoration: none; margin-top: 16px; padding: 8px 16px; background-color: lightslategray; color: white; border-radius: 8px;">Ir a la tienda -> </a></p>
                            </body>
                        </html>
                    """

    em.attach(MIMEText(mail_body, 'html'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, em.as_string())
        logging.info(f"Correo electrónico enviado correctamente a {receiver_email}")
        print(f"Correo electrónico enviado correctamente a {receiver_email}")
    except Exception as e:
        logging.info(f"No se pudo enviar el correo: {str(e)}")
        quit()

    server.quit()
