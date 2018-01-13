import usocket as socket
import ure as re
from http_parse import parse

class BasicHTTPHandler:

	def doGET(self, components, client, address, server):
		print('address:', address)
		print('components:', components)
		server.sendOK()

	def doPOST(self, components, client, address, server):
		print('address:', address)
		print('components:', components)
		stream = components[len(components) - 1]
		data = ''
		while True:
			line = stream.readline()[-2]
			if line == '' or not line:
				break
			data = data + line
		print('data:', data)
		server.sendOK()

class HTTPServer:

	def __init__(self, host = '0.0.0.0', port=80, handler=BasicHTTPHandler()):
		self.sock = socket.socket()
		addr = socket.getaddrinfo(host, port)[0][-1]
		self.sock.bind(addr)
		self.handler = handler

	def listen(self, no_of_connections=1):
		self.sock.listen(no_of_connections)

	"""
	accept() - wait for incoming connections
	"""
	def accept(self):
		client, addr = self.current = self.sock.accept()
		stream = client.makefile('rw', 0)
		results = parse(stream, client)
		handler = self.handler
		method = results[0]
		if method == 'POST':
			handler.doPOST(results, client, addr, self)
		elif method == 'GET':
			handler.doGET(results, client, addr, self)

	def send(self, status_code=200, message='OK'):
		client, _ = self.current
		client.send('HTTP/1.1 %s\r\n' % (status_code))
		client.send('Server: micropython_http_server (by deostroll)\r\n')
		client.send('\r\n')
		client.send('%s\r\n' % message)
		client.close()

	def sendOK(self):
		self.send()

	def writeln(self, message):
		client, _ = self.current
		client.send('%s\r\n' % message)


if __name__ == '__main__':
	server = HTTPServer(port=8080)
	server.listen()
	while True:
		server.accept()
