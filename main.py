import usocket as socket
# from machine import Pin
# import uselect
import ure as re

# led12 = Pin(12, Pin.OUT)
addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
# addr = ('0.0.0.0', 8080)

s = socket.socket()
s.bind(addr)
s.listen(1)

http_regex = re.compile(r'^(GET|POST)\s(\/(?:.+))\sHTTP\/\d\.\d')
header_regex = re.compile(r'^((?:(?:\w|\-))+)')

def _sanitize_(txt):
	if '-' in txt:
		idx = txt.find('-')
		return txt[0].toUpperCase() \
			+ txt[1 : idx] + '-' \
			 + txt[idx + 1].upper() \
			 + txt[idx + 2 : ]
	return txt

def parse(stream):
	line = stream.readline()
	method, path = http_regex.match(line).groups()

	headers = {}

	while True:
		line = stream.readline()
		if line == b'\r\n' or not line:
			break
		parts = header_regex.match(line).groups()
		headers[_sanitize_(parts[0])] = parts[1]

	if method == 'POST':
		return (method, path, headers, stream)

	return (method, path, headers, None)


while True:
	client, addr = s.accept()
	stream = client.makefile('rwb', 0)
	parsed = parse(stream)
	print(parsed)
	client.send('ok')
	client.close()



