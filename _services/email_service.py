# imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# returns formatted html for a match email
#   post: the reddit post (contains the url, title, and description)
#   user: the User to send the notification to
def get_reddit_match_html(post, user):
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
            <p>Hey {user.username}!</p>
            <p>VinylScraper is doing its job!  Found a post:</p>
            <p><b>Post title:</b><br> {title}<p>
            <p><b>{url_header}</b><br> {url}</p>
            <p><b>Post Description:</b><br> {description}</p>
        </body>
    </html>
    """
    return msg


# returns formatted html for page match email
#   search: the SearchUrl that we found
#   user: the User to send the notification to
def get_page_match_html(search, user):
    msg = f"""\
        <html>
            <head></head>
            <body>
                <p>Hey {user.username}!</p>
                <p>VinylScraper is doing its job!</p>
                <p><b>{search.product}</b> is either in stock or available!<p>
                <br>
                <p><b>URL to product:</b><br> {search.url}</p>
            </body>
        </html>
        """
    return msg


# returns formatted html for twitter patch email
#   found_keywords: the keywords that were found
#   tweet: the tweet we found
#   user: the User to send the notification to
def get_twitter_match_html(found_keywords, tweet, user):
    msg = f"""\
        <html>
            <head></head>
            <body>
                <p>Hey {user.username}!</p>
                <p>VinylScraper is doing its job!</p>
                <p>Found the keywords <b>{found_keywords}</b> in a tweet from {tweet.author_id}!<p>
                <br>
                <p><b>URL to tweet:</b><br> https://twitter.com/{tweet.author_id}/status/{tweet.id}</p>
            </body>
        </html>
        """
    return msg


# service class for emailing things
class EmailService:
    # port for ssl (but not really ssl?)
    port = 465

    # __init__
    def __init__(self, sender_email, sender_email_password, user_agent, logger):
        self.sender_email = sender_email
        self.sender_email_password = sender_email_password
        self.user_agent = user_agent
        self.logger = logger

    # actually sends the email
    # returns the result of the email sending (a dictionary object)
    #   email: the email to send to (can be either a list of emails or a string email)
    #   subject: the subject line of the email
    #   message_html: the message in html format
    def send_email(self, emails, subject, message_html):
        # build the email
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.user_agent + ' ' + self.sender_email
        msg['To'] = ", ".join(emails) if isinstance(emails, list) else emails
        msg.attach(MIMEText(message_html, 'html'))

        # send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', self.port) as server:
            server.login(self.sender_email, self.sender_email_password)
            return server.sendmail(self.sender_email, emails if isinstance(emails, list) else [emails], msg.as_string())

    # sends reddit match email
    #   keyword: the keyword that was found
    #   post: the post where we found the match
    #   user: the user that the match was found for
    def send_reddit_match_email(self, keyword, post, user):
        message_html = get_reddit_match_html(post, user)
        subject = f'VinylScraper: Reddit match found! ({keyword})'

        res = self.send_email(user.emails, subject, message_html)
        if res == {}:
            self.logger.info('EmailService', f'Successfully sent email on reddit match: {keyword}')
        else:
            self.logger.error('EmailService', f'Error in sending email on reddit match: {res}')

    # sends twitter match email
    #   found_keywords: the keywords that were found
    #   tweet: the tweet that matched
    #   user: the user that the match was found for
    def send_twitter_match_email(self, found_keywords, tweet, user):
        message_html = get_twitter_match_html(found_keywords, tweet, user)
        subject = f'VinylScraper: Twitter match found! ({found_keywords})'

        res = self.send_email(user.emails, subject, message_html)
        if res == {}:
            self.logger.info('EmailService', f'Successfully sent email on twitter match: {found_keywords}')
        else:
            self.logger.error('EmailService', f'Error in sending email on twitter match: {res}')

    # sends page match email
    #   search: the SearchUrl that we found
    #   user: the user that the match was found for
    def send_page_match_email(self, search, user):
        message_html = get_page_match_html(search, user)
        subject = f'VinylScraper: An item is available! ({search.product})'

        res = self.send_email(user.emails, subject, message_html)
        if res == {}:
            self.logger.info('EmailService', f'Successfully sent email on page match: {search.product}')
        else:
            self.logger.error('EmailService', f'Error in sending email on reddit match: {res}')
