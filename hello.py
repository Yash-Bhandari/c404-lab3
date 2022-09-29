#!/usr/bin/env python3

import os
import json
import cgi
import secret
from templates import _wrapper, login_page, secret_page
from os import environ


env_vars = dict(os.environ)
form = cgi.FieldStorage()

def serve_environment():
	print("Content-type: application/json")
	print()
	print(json.dumps(env_vars))

def request_info():
	print("Content-type: text/html")
	print()
	print(_wrapper(f"""
		QUERY_STRING: {env_vars['QUERY_STRING']} <br>
		Browser: {env_vars['HTTP_USER_AGENT']} <br>
	"""))

def parse_cookies():
	cookie_str = env_vars['HTTP_COOKIE']
	if cookie_str == '':
		return {}
	cookies = {}
	for kvp in cookie_str.split('; '):
		key, value = kvp.split('=')
		cookies[key] = value
	return cookies
	

def handle_login_attempt():
	username = form.getfirst('username')
	password = form.getfirst('password')

	
	if username == secret.username and password == secret.password:
		print("Content-type: text/html")
		print("Set-Cookie: auth=True")
		print("Set-Cookie: test_cookie=true")
		print()
		print(secret_page(username, password))
	else:
		print(login_page())

cookies = parse_cookies()
if os.environ['REQUEST_METHOD'] == 'POST':
	handle_login_attempt()
elif cookies.get('auth') == 'True':
	print(secret_page(secret.username, secret.password))
else:
	print(login_page())