from getpass import getpass
import os
import time
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

tokenTemp = None
class getTokenHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global tokenTemp
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'no')
        tokenTemp = self.path.replace('/', '')
        self.server.shutdown()

    def log_message(self, format, *args):
        return

def getConfig(needToken=True, new=False):
    user = token = None

    if not new and os.path.isfile('config.dat'):
        with open('config.dat', 'r') as f:
            t = f.read().splitlines()
            token = t[0]
            user = t[1]
        if needToken:
            r = requests.get('https://discord.com/api/v6/users/@me', headers=getHeader(token=token))
            if r.status_code == 200:
                user = r.json()
            else:
                token = None

    if not token:
        global tokenTemp
        cprint("Token invalid! Please paste the following command into your Discord Developer Tools (Ctrl + Shift + I): " + FG.brightgreen + "var xhttp = new XMLHttpRequest(); var f=document.body.appendChild(document.createElement('iframe'));f.src='/robots.txt';location.href='/channels/@me';f.onload=()=>{xhttp.open('GET', 'http://127.0.0.1:8123/' + f.contentWindow.localStorage.token.replace(/['\"]+/g,''), true); xhttp.send();}")
        n = 0
        tokenTemp = None
        httpd = HTTPServer(('127.0.0.1', 8123), getTokenHandler)
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()
        while not tokenTemp:
            n += 1
            if n > 60:
                cprint(f'{FG.red}Timeout after 60 seconds.')
                exit(1)
            time.sleep(1)
        token = tokenTemp
        user = requests.get('https://discord.com/api/v6/users/@me', headers=getHeader(token=token)).text.replace('\n', '')

        with open('config.dat', 'w') as f:
            f.write(f'{token}\n{user}')

    return {'token':token, 'user':user}


def getHeader(token=None):
    if not token:
        token = getConfig()['token']
    return {'sec-fetch-mode': 'cors',
    'host': 'discord.com',
    'origin': 'https://discord.com',
    'accept-language': 'en-US',
    'authorization': token,
    'x-super-properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkRpc2NvcmQgQ2xpZW50IiwicmVsZWFzZV9jaGFubmVsIjoiY2FuYXJ5IiwiY2xpZW50X3ZlcnNpb24iOiIwLjAuOTMiLCJvc192ZXJzaW9uIjoiNS4yLjgtMS1NQU5KQVJPIiwib3NfYXJjaCI6Ing2NCIsIndpbmRvd19tYW5hZ2VyIjoiaTMsaTMiLCJkaXN0cm8iOiJcIk1hbmphcm8gTGludXhcIiIsImNsaWVudF9idWlsZF9udW1iZXIiOjQ0MjgxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.93 Chrome/76.0.3809.110 Electron/6.0.2 Safari/537.36',
    'accept': '*/*',
    'content-type': 'application/json',
    'referer': 'https://discord.com/',
    'authority': 'discord.com',
    'sec-fetch-site': 'same-origin'}

class FG:
	black =			"\x1B[30m"
	red =			"\x1B[31m"
	green =			"\x1B[32m"
	yellow =		"\x1B[33m"
	blue =			"\x1B[34m"
	magenta =		"\x1B[35m"
	cyan =			"\x1B[36m"
	white =			"\x1B[37m"
	brightblack =	"\x1B[90m"
	brightred =		"\x1B[91m"
	brightgreen =	"\x1B[92m"
	brightyellow =	"\x1B[93m"
	brightblue =	"\x1B[94m"
	brightmagenta =	"\x1B[95m"
	brightcyan =	"\x1B[96m"
	brightwhite =	"\x1B[97m"

class Text:
	reset =			"\x1B[0m"
	bold =			"\x1B[1m"
	faint =			"\x1B[2m"
	italic =		"\x1B[3m"
	underline =		"\x1B[4m"
	blink =			"\x1B[5m"
	invert =		"\x1B[7m"
	conceal =		"\x1B[8m"
	strikethrough =	"\x1B[9m"
	franktur =		"\x1B[20m"
	framed =		"\x1B[51m"
	encircled =		"\x1B[52m"
	overlined =		"\x1B[53m"
	clear = 		"\x1B[2J"
	save =			"\x1B[s"
	restore =		"\x1B[u"

def cprint(value):
	"""Safely print with colors"""
	print(value, end=Text.reset + "\n")