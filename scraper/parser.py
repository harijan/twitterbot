from datetime import datetime
from html.parser import HTMLParser
from typing import TypedDict, List

class Tweet(TypedDict):
  is_retweet: bool
  header: str
  name: str
  handle: str
  tweet: str
  timestamp: str
  retrieved_time: float
  checked: str
  key: str

class TwitterParser(HTMLParser):
  start_tweet: bool
  start_tweet_retweet: bool
  start_tweet_header: bool
  start_tweet_name: bool
  start_tweet_handle: bool
  start_tweet_timestamp: bool
  start_tweet_content: bool
  retrieve_time: float
  current_tweet: Tweet
  tweets: List[Tweet]

  def __init__(self):
    self.tweets = []
    self.start_tweet = False
    self.start_tweet_retweet = False
    self.start_tweet_header = False
    self.start_tweet_name = False
    self.start_tweet_handle = False
    self.start_tweet_timestamp = False
    self.start_tweet_content = False
    self.retrieve_time = datetime.now().timestamp()
    self.current_tweet = {
      "is_retweet": False,
      "header": "",
      "name": "",
      "handle": "",
      "tweet": "",
      "timestamp": "",
      "checked": False,
      "key": "",
      "retrieved_time": self.retrieve_time
    }
    super().__init__()

  def handle_starttag(self, tag, attrs):
    if tag == "table":
      for k, v in attrs:
        v = v.rstrip() # spaces in class names
        if k == "class" and v == "tweet":
          self.start_tweet = True
          self.current_tweet: Tweet = {
            "is_retweet": False,
            "header": "",
            "name": "",
            "handle": "",
            "tweet": "",
            "timestamp": "",
            "checked": False,
            "key": "",
            "retrieved_time": self.retrieve_time
          }
    if self.start_tweet and tag == "tr":
      for k, v in attrs:
        v = v.rstrip() # spaces in class names
        if k == "class" and v == "tweet-content":
          self.start_tweet_retweet = True
        if k == "class" and v == "tweet-header":
          self.start_tweet_header = True
        if k == "class" and v == "tweet-container":
          self.start_tweet_content = True
    if self.start_tweet and self.start_tweet_header:
      for k, v in attrs:
        if k == "class" and v == "fullname":
          self.start_tweet_name = True
        if k == "class" and v == "username":
          self.start_tweet_handle = True
        if k == "class" and v == "timestamp":
          self.start_tweet_timestamp = True
    if self.start_tweet and self.start_tweet_content and tag == "div":
      for k, v in attrs:
        if k == "data-id":
          self.current_tweet["key"] = v

  def handle_endtag(self, tag):
    if tag == "table" and self.start_tweet:
      self.start_tweet = False
      for k,v in self.current_tweet.items():
        # print(f"key={k} type={type(self.current_tweet[k])} value={self.current_tweet[k]}")
        self.current_tweet[k] = self.current_tweet[k].strip() if type(self.current_tweet[k]) == str else self.current_tweet[k]
      self.tweets.append(self.current_tweet)
    if tag == "tr" and self.start_tweet_retweet:
      self.start_tweet_retweet = False
    if tag == "tr" and self.start_tweet_header:
      self.start_tweet_header = False
    if tag == "tr" and self.start_tweet_content:
      self.start_tweet_content = False
    if tag == "strong":
      self.start_tweet_name = False
    if tag == "div":
      self.start_tweet_handle = False
    if tag == "td":
      self.start_tweet_timestamp = False

  def handle_data(self, data:str):
    if self.start_tweet_retweet:
      if "retweeted" in data:
        self.current_tweet["is_retweet"] = True
        self.current_tweet["header"] = data
    if self.start_tweet_header:
      pass
      # print(f"Header data: {data}")
    if self.start_tweet_content:
      self.current_tweet["tweet"] = self.current_tweet["tweet"].strip() + " " + data.strip()
    if self.start_tweet_name:
      self.current_tweet["name"] += data
    if self.start_tweet_handle:
      self.current_tweet["handle"] += data
    if self.start_tweet_timestamp:
      self.current_tweet["timestamp"] += data
