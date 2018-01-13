import ure as re
import uos

print(dir(uos))

test = 'GET /foo HTTP/1.1'
test2 = 'Content-Type: application/json'

r1 = re.compile(r'^(GET|POST)\s(\/(?:.+))\sHTTP\/1\.1')
r2 = re.compile(r'^(.*)\:\s(.*)\r\n', re.)
matches = r1.match(test)
print(matches)
matches = r2.match(test2)
print(matches)

