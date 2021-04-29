import praw


class RedditService:

    def __init__(self, client_id, client_secret, user_agent):
        # create reddit instance
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent)

    # actually makes the call to reddit for new posts
    def get_new_posts(self, subreddit, post_count):
        return self.reddit.subreddit(subreddit).new(limit=post_count)

    # actually makes the call to reddit for hot posts
    def get_hot_posts(self, subreddit, post_count):
        return self.reddit.subreddit(subreddit).hot(limit=post_count)
