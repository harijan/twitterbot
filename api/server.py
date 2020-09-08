from http.server import HTTPServer
from api.handler import ApiHandler
from threading import Thread
from typing import Tuple, Dict
from scraper.parser import Tweet

class MyHTTPServer(HTTPServer):
  tweet_history: Dict[str, Tweet]

  def __init__(self, server_address, requesthandler, tweet_history):
    # self.server_address = server_address
    # self.RequestHandlerClass = requesthandler
    self.tweet_history = tweet_history
    super().__init__(server_address, requesthandler)

class ApiServer:
  http_thread: Thread
  http: MyHTTPServer
  port: int
  tweet_history: Dict[str, Tweet]

  def __init__(self, port: int, tweet_history: Dict[str, Tweet]):
    self.port = port
    self.tweet_history = tweet_history

    server_address: Tuple[str, int] = ('', self.port)
    self.http = MyHTTPServer(server_address, ApiHandler, tweet_history)

  def start_http_server(self):
    self.http_thread = Thread(None, self.http.serve_forever, "http_server")
    self.http_thread.start()

  def stop(self):
    self.http.shutdown()
    self.http_thread.join()
