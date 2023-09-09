import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_reset_password_email(email, full_name):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>TAKOMALL</title>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; color: #333;">
        <table cellpadding="0" cellspacing="0" width="100%" align="center" style="max-width: 600px; margin: 0 auto; background-color: #fff;">
            <tr>
                <td>
                    <table cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td style="background-color: #007bff; padding: 16px; text-align: center; color: #ffffff;">
                                <h1>TAKOMALL</h1>
                            </td>
                        </tr>
                    </table>
                    
                    <table cellpadding="20" cellspacing="0" width="100%">
                        <tr>
                            <td>
                                <h2 style="margin: 0;">Subject: Reset Your Password for Takomall</h2>
                                <p>Dear {full_name},</p>
                                <p>We received a request to reset your password for your Takomall account. To ensure the security of your account, please follow the button below to reset your password:</p>
                                <p><a href="{reset_link}" style="background-color: #007bff; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Reset password</a></p>
                                <p>If you didn't request to reset your password, please ignore this email. Your current password will remain unchanged.</p>
                                <p>Best regards,<br>The Takomall Team.</p>
                                <p>This email was sent to {email}. If you'd rather not receive this kind of email, you can unsubscribe or manage your email preferences.</p>
                                <p>© Takomall 2023</p>
                            </td>
                        </tr>
                    </table>
                    
                    <table cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td style="background-color: #007bff; padding: 16px; text-align: center; color: #ffffff;">
                                <p>TAKOMALL</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Create a message container (MIMEMultipart object)
    msg = MIMEMultipart()
    msg["From"] = "TAKOMALL <from@example.com>"
    msg["To"] = email
    msg["Subject"] = "Reset Your Password for Takomall"

    # Attach the HTML content
    msg.attach(MIMEText(html_template, "html"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("your_mailtrap_username", "your_mailtrap_password")
        server.sendmail(msg["From"], email, msg.as_string())

    print("Email sent successfully.")
