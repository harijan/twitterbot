from sched import scheduler
from argparse import ArgumentParser
from scraper.parser import Tweet
from scraper.twitter import Twitter
from typing import Dict, List, Optional
from time import time, sleep
from api.server import ApiServer
from datetime import datetime
import os

twitter = Twitter()
LINE_LENGTH = 80

def display_tweet(tweet: Tweet):
  top_string = datetime.now().isoformat()
  top_border: str = f"{top_string}{tweet['timestamp'].rjust(LINE_LENGTH-len(top_string),'-')}"
  header: str = ""
  if tweet["is_retweet"]:
    header += f"{tweet['header']}\n"
  header += f"{tweet['name']} [{tweet['handle']}]"
  body: str = tweet['tweet']
  bottom_border: str = "-" * LINE_LENGTH
  print(top_border, flush=True)
  print(header, flush=True)
  print(body, flush=True)
  print(bottom_border, flush=True)

def run(user: str, initial:Optional[bool] = False, interval: Optional[int] = None, s: Optional[scheduler] = None):
  tweets: List[Tweet] = twitter.get_tweets(user, initial=initial)
  for tweet in tweets:
    display_tweet(tweet)

  if len(tweets) == 0:
    print(f"{datetime.now().isoformat()} No new tweets!", flush=True)
  
  if interval and s:
    s.enter(interval, 1, run, argument=(user,), kwargs={"interval":interval, "s": s})

if __name__ == "__main__":
  parser:ArgumentParser = ArgumentParser(description="Scan the latest tweets of given user.")
  parser.add_argument("-u", "--user", default="", type=str, help="twitter handle you woant to display.")
  parser.add_argument("-i", "--interval", default=10*60, type=int, required=False, help="How quickly you want to recan tweets in seconds. [600]")
  parser.add_argument("-s", "--singleshot", default=False, action="store_true", help="just run a single time. [false]")
  parser.add_argument("--http", default=False, action="store_true", help="setup http server [false]")
  parser.add_argument("-p", "--port", default=8000, type=int, help="Setup port for http server [8000]")
  
  args: Dict = parser.parse_args()

  # overwrite defaults with environment variables
  if "TWITTER_USER" in os.environ:
    args.user = os.environ["TWITTER_USER"]
  
  print(f"Scanning user: {args.user}", flush=True)

  api_server: Optional[ApiServer] = None
  # setup API
  if args.http:
    api_server = ApiServer(args.port, twitter.tweet_history)
    api_server.start_http_server()

  s: scheduler = scheduler(time, sleep)
  run(args.user, initial=True)
  if not args.singleshot:
    s.enter(args.interval, 1, run, argument=(args.user,), kwargs={"interval":args.interval, "s": s})
    s.run()

  if api_server:
    api_server.stop()
  exit(0)