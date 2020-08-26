import os

class Config(object):
	SECRET_KEY=os.environ.get("SECRET KEY") or b'(Usi\xc8.\xea\xe51\xe553\x8c\xe1\x17\xa9'
	MONGODB_SETTINGS={'db':'Shopin'}