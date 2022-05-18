# imports
import tweepy


# main function
def main():
    api = tweepy.Client(
        bearer_token='AAAAAAAAAAAAAAAAAAAAAKwscAEAAAAAo5YxvP%2FMtC3pYuJM%2BS24cCaBkjA%3DEtfHIMRY7zBEdEnq8HKAGvXAe35vx9dMtkged5MnkCUxNLAXEH')
    user = 'iamdabinlee'
    query = f'from:{user}'

    tweets = api.search_recent_tweets(query=query, max_results=10)
    for tweet in tweets.data:
        print(f'https://twitter.com/{user}/status/{tweet.id}')
        print(tweet.text)


# still not 100% sure what this does, but it looks important
if __name__ == "__main__":
    main()
