# utils/email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_verification_code_email(display_name,email, verification_code):
    # Configure SMTP settings
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587  # Example port, adjust as needed
    smtp_username = 'bassemgog@gmail.com'
    smtp_password = 'efvq pnpf fihg nnfd' # app password form google

    # sender_email = 'noreply@dragna272.firebaseapp.com'
    # reply_to_email = 'noreply@dragna272.firebaseapp.com'
    sender_email = 'bassemgog@gmail.com'
    reply_to_email = 'bassemgog@gmail.com'
    subject = 'Verification Code for Your_App_Name'  # Update with your email subject

    # Customize email content
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject
    message.add_header('reply-to', reply_to_email)

    # HTML content with placeholders replaced by actual values
    # HTML content with inline styles
    # HTML content with inline styles
    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-top: 5px solid #4CAF50;
        }}
        .header {{
            background: linear-gradient(90deg, #4CAF50, #81C784);
            padding: 10px;
            border-radius: 10px 10px 0 0;
            color: #ffffff;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            padding: 20px;
            text-align: center;
        }}
        .content p {{
            font-size: 16px;
            color: #555555;
            margin: 10px 0;
        }}
        .verification-code {{
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            margin: 20px 0;
            background: #f9f9f9;
            padding: 10px;
            border-radius: 5px;
            display: inline-block;
        }}
        .footer {{
            padding: 10px;
            text-align: center;
            color: #999999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Email Verification</h1>
        </div>
        <div class="content">
            <div > <h1> Our app </h1> </div>
            <p>Hello <strong>{display_name}</strong>,</p>
            <p>Thank you for signing up for <strong>Your_App_Name</strong>. To complete your registration, please enter the verification code below:</p>
            <div class="verification-code">{verification_code}</div>
            <p>If you didn’t request this verification code, you can ignore this email.</p>
            <p>Thanks,</p>
            <p>Your <strong>Your_App_Name</strong> team</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 Your_App_Name. All rights reserved.</p>
        </div>
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
