# Assumptions:
 - include retweets.
 - decode tweets into utf-8
 - don't store results across runs
 - i think status id is time-ordered for the original tweet. but tweet list is ordered by retweet time - doesn't seem like we can scrape this time.
 - 
 - overwrite httpserver log so it doesn't pollute stdout. not a great idea.
 - when no new tweets are found - print out to stdout that no new tweets are found.

# command line usage:
```
usage: main.py [-h] [-u USER] [-i INTERVAL] [-s] [--http] [-p PORT]

Scan the latest tweets of given user.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  twitter handle you woant to display.
  -i INTERVAL, --interval INTERVAL
                        how quickly you want to recan tweets in seconds.
  -s, --singleshot      just run a single time.
  --http                setup http server.
  -p PORT, --port PORT  setup port for http server.
```
 
# docker file usage
## environment variables
```
TWITTER_USER - set the twitter user
```
the default port for the simple API is 8000

Sample docker run:
```
docker run --rm -p 8000:8000 -e TWITTER_USER=CriticalRole --name twitterbot twitterbot
```