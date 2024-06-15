# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText



# def send_ver_email(email, display_name, verification_link):
#     # Configure SMTP settings
#     smtp_host = 'smtp.gmail.com'
#     smtp_port = 587  # Example port, adjust as needed
#     smtp_username = 'bassemgog@gmail.com'
#     smtp_password = 'efvq pnpf fihg nnfd'

#     sender_email = 'noreply@dragna272.firebaseapp.com'
#     reply_to_email = 'noreply@dragna272.firebaseapp.com'
#     subject = 'Verify your email for Your_App_Name'  # Replace Your_App_Name with your actual app name
    
#     # Customize email content
#     message = MIMEMultipart()
#     message['From'] = sender_email
#     message['To'] = email
#     message['Subject'] = subject
#     message.add_header('reply-to', reply_to_email)

#     body = f"""Hello {display_name},

# Follow this link to verify your email address:

# {verification_link}

# If you didn’t ask to verify this address, you can ignore this email.

# Thanks,

# Your Your_App_Name team
# """
#     message.attach(MIMEText(body, 'plain'))

#     # Send email
#     try:
#         server = smtplib.SMTP(smtp_host, smtp_port)
#         server.starttls()
#         server.login(smtp_username, smtp_password)
#         server.sendmail(sender_email, email, message.as_string())
#         print('Email sent successfully.')
#     except Exception as e:
#         print(f'Failed to send email: {e}')
#     finally:
#         try:
#             server.quit()
#         except UnboundLocalError:
#             pass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#  this works
# def send_verification_code_email(email, name,code):
#     smtp_server = 'smtp.example.com'  # Replace with your SMTP server
#     smtp_port = 587  # Replace with your SMTP server's port number
#     smtp_username = 'your_email@example.com'  # Replace with your SMTP username
#     smtp_password = 'your_password'  # Replace with your SMTP password

#     sender_email = 'your_email@example.com'  # Replace with your email address
#     receiver_email = email
#     subject = 'Verification Code'

#     message = MIMEMultipart()
#     message['From'] = sender_email
#     message['To'] = receiver_email
#     message['Subject'] = subject

#     body = f"Your verification code is: {code}"
#     message.attach(MIMEText(body, 'plain'))

#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()
#     server.login(smtp_username, smtp_password)
    
#     try:
#         server.sendmail(sender_email, receiver_email, message.as_string())
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Error sending email: {e}")
#     finally:
#         server.quit()

# we will still try this from prexplixity 
def send_verification_code_email(email, name, code):
    smtp_server = 'smtp.example.com'  # Replace with your SMTP server
    smtp_port = 587  # Replace with your SMTP server's port number
    smtp_username = 'your_email@example.com'  # Replace with your SMTP username
    smtp_password = 'your_password'  # Replace with your SMTP password

    sender_email = 'your_email@example.com'  # Replace with your email address
    receiver_email = email
    subject = 'Verification Code'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    body = f"Your verification code is: {code}"
    message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    
    try:
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully.")
        server.quit()  # Move this line inside the try block
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        pass