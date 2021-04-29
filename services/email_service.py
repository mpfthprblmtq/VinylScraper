import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_html(post):
    title = post.title
    url = post.url
    description = post.selftext
    if 'www.reddit.com' in url:
        url_header = 'URL to post:'
    else:
        url_header = 'URL in post:'

    msg = f"""\
<html>
    <head></head>
    <body>
        <p>VinylScraper is doing its job!  Found a post:</p>
        <p><b>Post title:</b><br> {title}<p>
        <p><b>{url_header}</b><br> {url}</p>
        <p><b>Post Description:</b><br> {description}</p>
    </body>
</html>
"""
    return msg


class EmailService:

    # port for ssl (but not really ssl?)
    port = 465

    # __init__
    def __init__(self, receiver_email, sender_email, sender_email_password):
        self.receiver_email = receiver_email
        self.sender_email = sender_email
        self.sender_email_password = sender_email_password

    # sends the email
    def send_email(self, keyword, post):
        msg_html = get_html(post)

        msg = MIMEMultipart()
        msg['Subject'] = f'VinylScraper: Match found! ({keyword})'
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg.attach(MIMEText(msg_html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', self.port) as server:
            server.login(self.sender_email, self.sender_email_password)
            server.sendmail(self.sender_email, [self.receiver_email], msg.as_string())
            logging.info(f'{"EmailService".ljust(15)} : Successfully sent email on match: {keyword}')
            server.quit()
