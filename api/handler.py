from http.server import BaseHTTPRequestHandler
import json

class ApiHandler(BaseHTTPRequestHandler):
  def do_HEAD(self):
    self.send_response(200, "handle API Request")
    self.end_headers()

  def do_GET(self):
    # print("handle API Request")
    self.do_HEAD()
    tweets = { "tweets": [], "count": 0 }
    for k, v in self.server.tweet_history.items():
      tweets["tweets"].append(v)

    tweets["count"] = len(tweets["tweets"])
    response = bytearray(json.dumps(tweets), 'utf-8')
    self.wfile.write(response)
  
  # stop logging to stdout
  def log_message(self, format, *args):
    return