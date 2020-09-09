import json
from scraper.parser import Tweet
from api.handler import ApiHandler
from typing import Dict, IO, Tuple, List
from io import BytesIO as IO

def test_handler():
  class MockRequest(object):
    sent: bytes

    def __init__(self):
      self.sent = b''
    def makefile(self, *args, **kwargs):
      return IO(b"GET /")
    def sendall(self, b):
      self.sent += b
  class MockServer(object):
    tweet_history: Dict[str, Tweet]
    def __init__(self, ip_port, Handler, tweet_history):
      self.tweet_history = tweet_history
      handler = Handler(MockRequest(), ip_port, self)

  client_address: Tuple[str, int] = ('', 8000)
  # request:Request = Request('http://www.google.com')
  request = None
  tweet_history: Dict[str, Dict] = {
    '1300542258396106753': {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'Wido*GASP* this is incredible! 🔥 twitter.com/matthubelart/s…', 'timestamp': 'Aug 31', 'checked': False, 'key': '1300542258396106753'},
    '1303012984680329218': {'is_retweet': True, 'header': 'Critical Role retweeted', 'name': 'Pyu✨ @ FE3H hellhole', 'handle': '@pyudraws', 'tweet': 'I miss miss reani 😔✊🏻 #criticalrole #CriticalRoleArt @MicaBurton pic.twitter.com/LdJoMz6qaB', 'timestamp': '21h', 'checked': False, 'key': '1303012984680329218'},
    '1303018963836731397': {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'WEEKLY SCHEDULE ⚔️\n\nWhat new adventures await the Mighty Nein? Find out this Thursday with Critical Role Campaign 2, Episode 109! critrole.com/programming-sc…', 'timestamp': '20h', 'checked': False, 'key': '1303018963836731397'},
    '1303008993762095109': {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'COSPLAY GALLERY (September 2020)\n\nFeatured cosplay by @fangirlcrafter critrole.com/cosplay-galler… pic.twitter.com/p0quL6edQB', 'timestamp': '21h', 'checked': False, 'key': '1303008993762095109'},
  }
  tweet_list: List[Dict] = [
    {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'Wido*GASP* this is incredible! 🔥 twitter.com/matthubelart/s…', 'timestamp': 'Aug 31', 'checked': False, 'key': '1300542258396106753'},
    {'is_retweet': True, 'header': 'Critical Role retweeted', 'name': 'Pyu✨ @ FE3H hellhole', 'handle': '@pyudraws', 'tweet': 'I miss miss reani 😔✊🏻 #criticalrole #CriticalRoleArt @MicaBurton pic.twitter.com/LdJoMz6qaB', 'timestamp': '21h', 'checked': False, 'key': '1303012984680329218'},
    {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'WEEKLY SCHEDULE ⚔️\n\nWhat new adventures await the Mighty Nein? Find out this Thursday with Critical Role Campaign 2, Episode 109! critrole.com/programming-sc…', 'timestamp': '20h', 'checked': False, 'key': '1303018963836731397'},
    {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'COSPLAY GALLERY (September 2020)\n\nFeatured cosplay by @fangirlcrafter critrole.com/cosplay-galler… pic.twitter.com/p0quL6edQB', 'timestamp': '21h', 'checked': False, 'key': '1303008993762095109'},
  ]
  request:MockRequest = MockRequest()
  apiserver:MockServer = MockServer(('0.0.0.0', 8000), ApiHandler, tweet_history)
  apihandler = ApiHandler(request, client_address, apiserver)
  # apihandler.do_GET()
  # should_be_response = json.dumps({ 'tweets': tweet_list, 'count': len(tweet_list) }).encode('utf-8')
  response_json = request.sent.decode('utf-8')
  response = json.loads(response_json)
  assert(response["tweets"] == tweet_list)
  assert(response["count"] == len(tweet_history))

  updated_tweet_history: Dict[str, Dict] = {
    '1301626214034083842': {'is_retweet': True, 'header': 'Critical Role retweeted', 'name': 'Wyrmwood', 'handle': '@WyrmwoodGaming', 'tweet': 'pic.twitter.com/g7zmFlXkxJ', 'timestamp': 'Sep 3', 'checked': False, 'key': '1301626214034083842'},
    '1301561719345602560': {'is_retweet': True, 'header': 'Critical Role retweeted', 'name': 'LaTia, Overwhelmed™', 'handle': '@LaTiaJacquise', 'tweet': "oh my gosh you guys. \n\nYours truly is hopping into the DM's seat that Saturday at 12pm PST/2pm CST, and @ChrisPerkinsDnD , @quiddie , @CarlosCrits , @DoubleGXG , @Jody_Houser , and @VoiceOfOBrien have NO IDEA what they're about to get into.\n\nIt's gonna be SO. MUCH. FUN. twitter.com/Wizards_DnD/st…", 'timestamp': 'Sep 3', 'checked': False, 'key': '1301561719345602560'},
    '1300132378648571904': {'is_retweet': True, 'header': 'Critical Role retweeted', 'name': 'Rachel McEwan', 'handle': '@RachelMcEwanArt', 'tweet': 'Just felt like drawing Yasha...again #CriticalRoleArt #Criticalrole #criticalrolefanart pic.twitter.com/WJU4DZYXuT', 'timestamp': 'Aug 30', 'checked': False, 'key': '1300132378648571904'},
    '1301550869935079426': {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'Replying to @OutRightIntl $13 of each Don’t Forget to Love Each Other Shirt preordered in our Australia shop will benefit @OutRightIntl , an incredible nonprofit organization dedicated to fighting for the rights of LGBTQIA+ folks around the world. 🌈✨', 'timestamp': 'Sep 3', 'checked': False, 'key': '1301550869935079426'},
  }
  updated_tweet_list: List[Dict] = [
    {'is_retweet': True, 'header': 'Critical Role retweeted', 'name': 'Wyrmwood', 'handle': '@WyrmwoodGaming', 'tweet': 'pic.twitter.com/g7zmFlXkxJ', 'timestamp': 'Sep 3', 'checked': False, 'key': '1301626214034083842'},
    {'is_retweet': True, 'header': 'Critical Role retweeted', 'name': 'LaTia, Overwhelmed™', 'handle': '@LaTiaJacquise', 'tweet': "oh my gosh you guys. \n\nYours truly is hopping into the DM's seat that Saturday at 12pm PST/2pm CST, and @ChrisPerkinsDnD , @quiddie , @CarlosCrits , @DoubleGXG , @Jody_Houser , and @VoiceOfOBrien have NO IDEA what they're about to get into.\n\nIt's gonna be SO. MUCH. FUN. twitter.com/Wizards_DnD/st…", 'timestamp': 'Sep 3', 'checked': False, 'key': '1301561719345602560'},
    {'is_retweet': True, 'header': 'Critical Role retweeted', 'name': 'Rachel McEwan', 'handle': '@RachelMcEwanArt', 'tweet': 'Just felt like drawing Yasha...again #CriticalRoleArt #Criticalrole #criticalrolefanart pic.twitter.com/WJU4DZYXuT', 'timestamp': 'Aug 30', 'checked': False, 'key': '1300132378648571904'},
    {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'Replying to @OutRightIntl $13 of each Don’t Forget to Love Each Other Shirt preordered in our Australia shop will benefit @OutRightIntl , an incredible nonprofit organization dedicated to fighting for the rights of LGBTQIA+ folks around the world. 🌈✨', 'timestamp': 'Sep 3', 'checked': False, 'key': '1301550869935079426'},
  ]
  tweet_history.update(updated_tweet_history)
  tweet_list.extend(updated_tweet_list)

  assert(apiserver.tweet_history == tweet_history)

  updatedrequest:MockRequest = MockRequest()
  newapihandler:ApiHandler = ApiHandler(updatedrequest, client_address, apiserver)
  # should_be_response = json.dumps({ 'tweets': tweet_list, 'count': len(tweet_list) }).encode('utf-8')
  response_json = updatedrequest.sent.decode('utf-8')
  response = json.loads(response_json)
  assert(response["tweets"] == tweet_list)
  assert(response["count"] == len(tweet_history))