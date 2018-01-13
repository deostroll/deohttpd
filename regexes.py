import ure as re

http_regex = re.compile(r'^(GET|POST)\s(.*)\sHTTP\/1\.1')
header_regex = re.compile(r'^(.*)\:\s(.*)')
