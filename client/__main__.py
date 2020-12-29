from autobahn.twisted.websocket import WebSocketClientProtocol

class MyClientProtocol(WebSocketClientProtocol):

   def onOpen(self):
      self.sendMessage(u"Hello, world!".encode('utf8'))

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {0} bytes".format(len(payload)))
      else:
         print("Text message received: {0}".format(payload.decode('utf8')))

if __name__ == '__main__':

   import sys

   from twisted.python import log
   from twisted.internet import reactor
   log.startLogging(sys.stdout)

   from autobahn.twisted.websocket import WebSocketClientFactory
   factory = WebSocketClientFactory()
   factory.protocol = MyClientProtocol

   reactor.connectTCP("127.0.0.1", 4000, factory)
   reactor.run()
