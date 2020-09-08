from http.client import HTTPResponse
import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen, Request
from typing import Dict, Optional, List
from scraper.parser import Tweet, TwitterParser
import sqlite3

class Twitter:
  tweet_history: Dict[str, Tweet] = {}

  def get_only_new_tweets(self, tweets: List[Tweet], initial: Optional[bool]) -> List[Tweet]:
    new_tweets: List[Tweet] = []

    for tweet in tweets:
      if tweet["key"] not in self.tweet_history:
        new_tweets.append(tweet)
      # print(f"tweet={tweet} type={type(tweet['key'])}")
      self.tweet_history[tweet["key"]] = tweet

    #status is time ordered?
    new_tweets.sort(key=lambda x: x["key"], reverse=True)
    num = 5 if initial else len(tweets)
    # print(f"num={num} tweets={new_tweets} len={len(tweets)}")
    return new_tweets[:num]

  def get_tweets(self, user, initial=False):
    ret: Dict[str, str] = { }
    url = f"https://mobile.twitter.com/{user}/"

    # request: Request = Request(url, None)
    response: Optional[HTTPResponse] = None
    try:
      response = urlopen(url)
      body: str = response.read().decode('utf-8')
      twitter_parser: TwitterParser = TwitterParser()
      twitter_parser.feed(body)
      tweets = twitter_parser.tweets
      ret = self.get_only_new_tweets(tweets, initial)
      twitter_parser.tweets = []
    except URLError as e:
      print(f"URLError: {e}", flush=True)

    return ret