# deohttpd

this is a webserver program meant to run within esp8266. 

Written in MicroPython.

This is a very basic server implementation. Modelled after
HTTPServer, and BaseHTTPServer (from python standard library)

The usage too is somewhat similar.

Example:

```
from deohttpd import BasicHTTPHandler, HTTPServer as Server

class MyHandler(BasicHTTPHandler):
	def doGET(self, request, server):
		path = request[1]

		if path == '/foo':
			# do someting here
			server.send_ok()
		elif path == '/bar':
			# do something else here
			server.send_ok()
		else:
			# serve 404
			server.send(status_code=404, message='The thing you are looking for probably vanished!!!')
			

		server.close()

	def doPOST(self, request, server):
		if path == '/catfish':
			# xxx-form-urlencoded data
			data = request[3]
			some_value = data['some_key']
			# launch unicorns with some_value
			server.send_ok()
		else:
			#serve the 404 message...



server = Server(host='0.0.0.0', port=80, handler=MyHTTPHandler())
server.listen()

while True:
	
	# blocks for incoming request
	server.accept()

```

Thats it!!!

More info if you can lookup in the source code.

Note: this server can receive any simple form data posted to it (http POST)

