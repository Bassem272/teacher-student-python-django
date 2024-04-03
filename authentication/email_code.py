# utils/email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_verification_code_email(display_name,email, verification_code):
    # Configure SMTP settings
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587  # Example port, adjust as needed
    smtp_username = 'bassemgog@gmail.com'
    smtp_password = 'efvq pnpf fihg nnfd'

    sender_email = 'noreply@dragna272.firebaseapp.com'
    reply_to_email = 'noreply@dragna272.firebaseapp.com'
    subject = 'Verification Code for Your_App_Name'  # Update with your email subject

    # Customize email content
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject
    message.add_header('reply-to', reply_to_email)

      # HTML content with placeholders replaced by actual values
    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification</title>
</head>
<body>
    <div>
        <h1>Email Verification</h1>
        <p>Hello <strong>{display_name}</strong>,</p>
        <p>Thank you for signing up for <strong>Your_App_Name</strong>. To complete your registration, please enter the verification code below:</p>
        <div><strong>{verification_code}</strong></div>
        <p>If you didn’t request this verification code, you can ignore this email.</p>
        <p>Thanks,</p>
        <p>Your <strong>Your_App_Name</strong> team</p>
    </div>
</body>
</html>
"""

    message.attach(MIMEText(body, 'html'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, email, message.as_string())
        print('Email sent successfully.')
    except Exception as e:
        print(f'Failed to send email: {e}')
    finally:
        server.quit()
