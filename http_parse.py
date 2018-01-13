import regexes as re
import logger

class CONSTS:
	NEW_LINE = '\r\n'

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

def parse(client):
	client_stream = client.makefile('rwb', 0)
	bline = client_stream.readline()
	line = bline.decode('utf-8')
	match = re.http_regex.match(line)
	if match:
		method = match.group(1)
		path = match.group(2)
	else:
		log.error('Invalid header start')
		client_stream.close()

	log.verb('parsing headers...')
	headers = {}
	while True:
		bline = client_stream.readline()
		line = bline.decode('utf-8')
		if line == '\r\n' or not line:
			break
		
		if CONSTS.NEW_LINE in line : line = line[:-2]

		match = re.header_regex.match(line)
		
		if match:
			key = _sanitize_(match.group(1))
			value = match.group(2)
			headers[key] = value
		else:
			log.error('could not parse header line: %s' % line)
	
	data = None
	
	if method == 'POST' and line:
		length = int(headers['Content-Length'])
		log.verb('Reading post data...')
		data = client_stream.read(length)
		log.verb('data received: %s' % data)

	result = (method, path, headers, data)
	
	log.verb('Parsed: %s' % ( str(result) ))
	return result
