import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 假冒的發件人和受害者
sender_email = "fakeemail@example.com"
receiver_email = "victim@example.com"
subject = "Account Verification Required"
body = """
Dear User,

We have detected unusual activity on your account. Please click the link below to verify your account:

http://fakebank.com/verify?user=victim

Thank you,
Fake Bank Support
"""

# 設定SMTP伺服器
smtp_server = "smtp.example.com"
smtp_port = 587
smtp_user = "smtp_user@example.com"
smtp_password = "smtp_password"

# 創建MIME對象
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# 發送電子郵件
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("Phishing email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()
