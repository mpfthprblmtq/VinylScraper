# VinylScraper

### What is it
A scraping bot used to get the newest reddit posts on r/VinylReleases.

### How to use it
Follow the instructions laid out [here](https://towardsdatascience.com/scraping-reddit-data-1c0af3040768) in the "Getting Started" section.  When you have the client_id, secret, and name, throw those values in the `default_app_info.txt` for the client_id, client_secret, and user_agent, respectively.

You'll need to create an email that you can send emails from.  You can follow [these steps](https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development) to create a gmail account for development.
Once you have that email created, fill the `default_app_info.txt` file with that information.  `sender_email` should be where the emails are coming from, so the email you just created.  `receiving_email` should be wherever you want these emails sent to. `sender_email_password` is the plaintext password for the email account you just created.

Now that your `default_app_info.txt` file has all the information it needs, rename that file to `app_info.txt` so the bot can read it.

Finally, fill the keywords.txt file with keywords you want to search for in the reddit posts.  Each keyword should be on its own line.