from deohttpd import HTTPServer as Server, BasicHTTPHandler
from machine import Pin

led12 = Pin(12, Pin.OUT)

class TriggerHTTPHandler(BasicHTTPHandler):

	def doGET(self, request, server):
		path = request[1]

		if path == '/on':
			led12.on()
		else:
			led12.off()

		server.send_ok()

	def doPOST(self, request, server):
		server.send_method_not_allowed()

handler = TriggerHTTPHandler()

server = Server(handler=handler)
server.listen()

print('Server running on port:', server.port)
while True:
	server.accept()