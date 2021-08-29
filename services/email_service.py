import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import platform


# returns formatted html for a match email
def get_reddit_match_html(post, uptime):
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
            <br>
            <p><b>Uptime:</b> {uptime}</p>
        </body>
    </html>
    """
    return msg


# returns formatted html for page match email
def get_page_match_html(search, user, uptime):
    msg = f"""\
        <html>
            <head></head>
            <body>
                <p>Hey {user.username}, VinylScraper is doing its job!</p>
                <p><b>{search.product}</b> is either in stock or available!<p>
                <br>
                <p><b>URL to product:</b><br> {search.url}</p>
                <br>
                <p><b>Uptime:</b> {uptime}</p>
            </body>
        </html>
        """
    return msg


# returns formatted html for a startup email
def get_startup_html():
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    return f"""\
    <html>
        <head></head>
        <body>
            <h3>Vinyl Scraper started up! ({platform.system()})</h3>
            <p><b>Start time:</b> {dt_string}</p>
        </body>
    </html>
    """


# returns formatted html for a shutdown email
def get_shutdown_html(e, uptime):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return f"""\
    <html>
        <head></head>
        <body>
            <h3>Vinyl Scraper shut down!</h3>
            <p><b>End time:</b> {dt_string}</p>
            <p><b>Uptime:</b> {uptime}</p>
            <br>
            <p><b>Exception Details:<b></p>
            <p>{e}</p>
        </body>
    </html>
    """


class EmailService:
    # port for ssl (but not really ssl?)
    port = 465

    # __init__
    def __init__(self, sender_email, sender_email_password, user_agent, uptime_service):
        self.sender_email = sender_email
        self.sender_email_password = sender_email_password
        self.user_agent = user_agent
        self.uptime_service = uptime_service

    # sends reddit match email
    def send_reddit_match_email(self, keyword, post, user):
        msg_html = get_reddit_match_html(post, self.uptime_service.get())

        msg = MIMEMultipart()
        msg['Subject'] = f'VinylScraper: Match found! ({keyword})'
        msg['From'] = self.user_agent + ' ' + self.sender_email
        msg['To'] = user.email
        msg.attach(MIMEText(msg_html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', self.port) as server:
            server.login(self.sender_email, self.sender_email_password)
            server.sendmail(self.sender_email, [user.email], msg.as_string())
            logging.info(f'{"EmailService".ljust(18)} : Successfully sent email on match: {keyword}')

    # sends page match email
    def send_page_match_email(self, search, user):
        msg_html = get_page_match_html(search, user, self.uptime_service.get())

        msg = MIMEMultipart()
        msg['Subject'] = f'VinylScraper: An item is available! ({search.product})'
        msg['From'] = self.user_agent + ' ' + self.sender_email
        msg['To'] = user.email
        msg.attach(MIMEText(msg_html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', self.port) as server:
            server.login(self.sender_email, self.sender_email_password)
            server.sendmail(self.sender_email, [user.email], msg.as_string())
            logging.info(f'{"EmailService".ljust(18)} : Successfully sent email on match: {search.product}')

    # sends an email on startup
    def send_startup_email(self, receiver_email):
        msg_html = get_startup_html()

        msg = MIMEMultipart()
        msg['Subject'] = f'VinylScraper: Startup'
        msg['From'] = self.user_agent + ' ' + self.sender_email
        msg['To'] = receiver_email
        msg.attach(MIMEText(msg_html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', self.port) as server:
            server.login(self.sender_email, self.sender_email_password)
            server.sendmail(self.sender_email, [receiver_email], msg.as_string())
            logging.info(f'{"EmailService".ljust(18)} : Successfully sent startup email')

    # sends an email on shutdown
    def send_shutdown_email(self, e, receiver_email):
        msg_html = get_shutdown_html(e, self.uptime_service.get())

        msg = MIMEMultipart()
        msg['Subject'] = f'VinylScraper: Shutdown'
        msg['From'] = self.user_agent + ' ' + self.sender_email
        msg['To'] = receiver_email
        msg.attach(MIMEText(msg_html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', self.port) as server:
            server.login(self.sender_email, self.sender_email_password)
            server.sendmail(self.sender_email, [receiver_email], msg.as_string())
            logging.info(f'{"EmailService".ljust(18)} : Successfully sent shutdown email')
            server.quit()
