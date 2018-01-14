import usocket as socket
import ure as re
from http_parse import parse
import logger

log = logger.Logger('server', logger.LOG_LEVEL.VERB)

class BasicHTTPHandler:

	def doGET(self, components, server):
		log.verb('Handling get with path: %s' % components[1])
		server.send_ok()

	def doPOST(self, components, server):
		data = components[len(components) - 1]
		log.verb('Handling post with data: %s' % data)
		server.send_ok()

class HTTPServer:

	def __init__(self, host = '0.0.0.0', port=80, handler=BasicHTTPHandler()):
		self.sock = socket.socket()
		addr = socket.getaddrinfo(host, port)[0][-1]
		self.sock.bind(addr)
		self.handler = handler
		self.port = port
		
	def listen(self, no_of_connections=1):
		self.sock.listen(no_of_connections)

	"""
	accept() - wait for incoming connections
	"""
	def accept(self):
		client, addr = self.current = self.sock.accept()
		# log.verb('Connected from: %s' % str(bytes(addr)) )
		self._closed = False
		log.verb('Connection received...')
		parsed = parse(client)
		self.process(parsed)

	def send(self, status_code=200, message='OK'):
		# client, _ = self.current
		self.writeln('HTTP/1.1 %s' % status_code)
		self.writeln('Server: deohttpd (MicroPython)')
		self.writeln('')
		self.writeln('%s' % message)
		

	def send_ok(self):
		if not self._closed:
			self.send()
			self.close()

	def writeln(self, message):
		client, _ = self.current
		client.send('%s\r\n' % message)

	def close(self):
		client, _ = self.current
		if not self._closed:
			log.verb('Closing connection...')
			client.close();
			self._closed = True

	def process(self, results):
		handler = self.handler
		method = results[0]
		if method == 'GET':
			handler.doGET(results, self)
		elif method == 'POST':
			handler.doPOST(results, self)
		else:
			self.send_method_not_allowed()

	def send_method_not_allowed(self):
		if not self._closed:
			self.send(status_code=405, message='Method not allowed')
			self.close()

def test():

	server = HTTPServer(port=8080)
	server.listen()
	print('running on port 8080...')
	
	while True:
		server.accept()

if __name__ == '__main__':

	test()
