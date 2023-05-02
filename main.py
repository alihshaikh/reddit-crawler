import config
import praw

reddit = praw.Reddit(
    client_id= config.clientID,
    client_secret=config.clientSecret,
    user_agent=config.clientSecret,
)


ucr_subreddit = reddit.subreddit("ucr")

for post in ucr_subreddit.hot(limit=10):
    print(post.title)