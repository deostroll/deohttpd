import network
import ujson

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

sta.active(False)
ap.active(True)

credentials = ujson.loads(open('credentials.json', 'r').read())
print('credentials:', credentials)
ap.config(essid=credentials['wifi_name'], password=credentials['wifi_password'])

print('configuration:', ap.ifconfig())