# imports
import smtplib
import platform
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# returns formatted html for a match email
#   post: the reddit post (contains the url, title, and description)
#   uptime: the current uptime
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
#   search: the SearchUrl that we found
#   user: the User to send the notification to
#   uptime: the current uptime
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
#   e: the exception that occurred
#   uptime: the current uptime
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


# service class for emailing things
class EmailService:
    # port for ssl (but not really ssl?)
    port = 465

    # __init__
    def __init__(self, sender_email, sender_email_password, user_agent, uptime_service, logger):
        self.sender_email = sender_email
        self.sender_email_password = sender_email_password
        self.user_agent = user_agent
        self.uptime_service = uptime_service
        self.logger = logger

    # actually sends the email
    # returns the result of the send (a dictionary object)
    #   email: the email to send to
    #   subject: the subject line of the email
    #   message_html: the message in html format
    def send_email(self, email, subject, message_html):
        # build the email
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.user_agent + ' ' + self.sender_email
        msg['To'] = email
        msg.attach(MIMEText(message_html, 'html'))

        # send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', self.port) as server:
            server.login(self.sender_email, self.sender_email_password)
            return server.sendmail(self.sender_email, [email], msg.as_string())

    # sends reddit match email
    #   keyword: the keyword that was found
    #   post: the post where we found the match
    #   user: the user that the match was found for
    def send_reddit_match_email(self, keyword, post, user):
        message_html = get_reddit_match_html(post, self.uptime_service.get())
        subject = f'VinylScraper: Match found! ({keyword})'

        res = self.send_email(user.email, subject, message_html)
        if res == {}:
            self.logger.info('EmailService', f'Successfully sent email on reddit match: {keyword}')
        else:
            self.logger.error('EmailService', f'Error in sending email on reddit match: {res}')

    # sends page match email
    #   search: the SearchUrl that we found
    #   user: the user that the match was found for
    def send_page_match_email(self, search, user):
        message_html = get_page_match_html(search, user, self.uptime_service.get())
        subject = f'VinylScraper: An item is available! ({search.product})'

        res = self.send_email(user.email, subject, message_html)
        if res == {}:
            self.logger.info('EmailService', f'Successfully sent email on page match: {search.product}')
        else:
            self.logger.error('EmailService', f'Error in sending email on reddit match: {res}')

    # sends an email on startup
    #   email: the email to send the startup email to
    def send_startup_email(self, email):
        message_html = get_startup_html()
        subject = f'VinylScraper: Startup'

        res = self.send_email(email, subject, message_html)
        if res == {}:
            self.logger.info('EmailService', f'Successfully sent startup email')
        else:
            self.logger.error('EmailService', f'Error in sending startup email: {res}')

    # sends an email on shutdown
    #   e: the exception that caused the shutdown
    #   email: the email to send the shutdown email to
    def send_shutdown_email(self, e, email):
        message_html = get_shutdown_html(e, self.uptime_service.get())
        subject = f'VinylScraper: Shutdown'

        res = self.send_email(email, subject, message_html)
        if res == {}:
            self.logger.info('EmailService', f'Successfully sent shutdown email')
        else:
            self.logger.error('EmailService', f'Error in sending shutdown email: {res}')
