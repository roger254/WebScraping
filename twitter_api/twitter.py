from twitter import OAuth
from twitter.api import Twitter

t = Twitter(auth=OAuth(
    "546031799-12xBlqfXjCBU3JeQyIwUUJRjFxoHlPmar56T6Tuq",
    "Y3eoO4DFeflE4nzeqTIpiRZfTsghEWXdo40CLGkFrFnFE",
    "CJhCbqDigv1S8Y24kfbw4EuQd",
    "lSsQ6cDhACA3mn3UYmksAe0S7vPLvGjvcnAlA3k3Bp9LQYgFDq")
)

python_tweets = t.search.tweets(q="#python", count=10)
print(python_tweets)
