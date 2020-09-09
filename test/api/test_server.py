from http.server import BaseHTTPRequestHandler
from api.server import ApiServer
from typing import Dict

def test_server():
  class MockHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
      self.send_response(200)
      self.end_headers()

    def do_GET(self):
      # print("handle API Request")
      self.do_HEAD()
      self.wfile.write("mockhandler")
  
  tweet_history: Dict[str, Dict] = {
    '1300542258396106753': {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'Wido*GASP* this is incredible! 🔥 twitter.com/matthubelart/s…', 'timestamp': 'Aug 31', 'checked': False, 'key': '1300542258396106753'},
    '1303012984680329218': {'is_retweet': True, 'header': 'Critical Role retweeted', 'name': 'Pyu✨ @ FE3H hellhole', 'handle': '@pyudraws', 'tweet': 'I miss miss reani 😔✊🏻 #criticalrole #CriticalRoleArt @MicaBurton pic.twitter.com/LdJoMz6qaB', 'timestamp': '21h', 'checked': False, 'key': '1303012984680329218'},
    '1303018963836731397': {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'WEEKLY SCHEDULE ⚔️\n\nWhat new adventures await the Mighty Nein? Find out this Thursday with Critical Role Campaign 2, Episode 109! critrole.com/programming-sc…', 'timestamp': '20h', 'checked': False, 'key': '1303018963836731397'},
    '1303008993762095109': {'is_retweet': False, 'header': '', 'name': 'Critical Role', 'handle': '@CriticalRole', 'tweet': 'COSPLAY GALLERY (September 2020)\n\nFeatured cosplay by @fangirlcrafter critrole.com/cosplay-galler… pic.twitter.com/p0quL6edQB', 'timestamp': '21h', 'checked': False, 'key': '1303008993762095109'},
  }
  server: ApiServer = ApiServer(8000, tweet_history)
  server.start_http_server()
  assert(server.http_thread.is_alive() == True)
  server.stop()
  assert(server.http_thread.is_alive() == False)