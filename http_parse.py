import ure as re

http_regex = re.compile(r'^^(GET|POST)\s(.*)\sHTTP\/1\.1')
header_regex = re.compile(r'^(.*)\:\s(.*)')

import logger

log = logger.Logger('parser', logger.LOG_LEVEL.VERB)

def _sanitize_(txt):
	txt = str(txt)
	if '-' in txt:
		idx = txt.find('-')
		return txt[0].upper() \
			+ txt[1 : idx] + '-' \
			 + txt[idx + 1].upper() \
			 + txt[idx + 2 : ]
	return txt

def parse(stream, client):
	line = stream.readline()
	log.verb('line: %s' % line)
	match = http_regex.match(line)
	method, path = (match.group(1), match.group(2))
	log.verb('method: %s, path: %s' %(method, path))
	headers = {}
	log.verb('parsing headers...')
	while True:
		line = stream.readline()
		log.verb('line: %s, type: %s' \
			% (line, str(type(line)) ))
		if line == '\r\n' or not line:
			break
		match = header_regex.match(line)
		log.verb(match)
		parts = (match.group(1), match.group(2)[:-2])
		headers[_sanitize_(parts[0])] = parts[1]

	log.verb('headers: %s' % headers)

	if method == 'POST':
		content_type = headers['Content-Type']
		if content_type == 'application/x-www-form-urlencoded':
			log.verb('parsing urlencoded data...')
			stream.close()
			arr = client.read(4096)
			log.verb('received: %s' % (len(arr)))
		return (method, path, headers, stream)

	return (method, path, headers, None)

