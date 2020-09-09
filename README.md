# Assumptions:
 - only use python standard library, except for the test framework.
 - to run the tests, use the requirements.txt or just install pytest
    - ```pip install pytest```
    - run ```pytest``` from the project root directory.
 - include retweets.
 - decode tweets into utf-8
 - don't store results across runs
 - i think status id is time-ordered for the original tweet - not much documentation on it. (https://developer.twitter.com/en/docs/twitter-ids)
 - tweet list is ordered by retweet time - doesn't seem like we can scrape it or we could with some jangling.
 - overwrite httpserver log so it doesn't pollute stdout. it probably doesn't matter too much, but hey ¯\\\_(ツ)\_/¯
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
or use the included docker-compose
```
docker-compose -f docker-compose.yml up -d
```

stuff is printed out to stdout -  so use ```docker logs [-f] [container]``` to check them out.