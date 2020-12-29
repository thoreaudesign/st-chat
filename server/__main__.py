from autobahn.twisted.websocket import WebSocketServerProtocol

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        # s = payload.decode('utf-8')
        # s = payload.encode('utf-8')
        ## echo back message verbatim
        self.sendMessage(payload, isBinary)
        #self.sendMessage(payload, isBinary = False)

    def onOpen(self):
        print("WebSocket connection open.")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

if __name__ == '__main__':

    import sys
    
    from twisted.python import log
    from twisted.internet import reactor
    log.startLogging(sys.stdout)
    
    from autobahn.twisted.websocket import WebSocketServerFactory
    factory = WebSocketServerFactory()
    factory.protocol = MyServerProtocol
    
    reactor.listenTCP(4000, factory)
    reactor.run()
