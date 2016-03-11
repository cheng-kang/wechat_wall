#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import pymongo

define("port", default=8003, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/auth", AuthHandler),
			(r"/form", FormHandler),
			(r"/api", ApiHandler),
			(r"/host", HostHandler),
			(r"/log", LogHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			)
		conn = pymongo.Connection("localhost", 27017)
		self.db = conn["wechatwall"]
		tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html",)


class FormHandler(tornado.web.RequestHandler):
	def get(self):
		nickname = self.get_cookie("nickname", None)
		self.render("form.html",nickname = nickname)

	def post(self):
		import random
		content = self.get_argument('content', None)
		msg = dict()
		if content:
			coll = self.application.db.msg
			last = coll.find().sort("id",pymongo.DESCENDING).limit(1)
			lastone = dict()
			lastone['id'] = 0
			if last:
				for item in last:
					lastone = item
			msg['id'] = int(lastone['id']) + 1

			random = random.randrange(1,11)
			avatar = "http://suosikeji.qiniudn.com/wulian_"+str(random)+".jpg"
			msg['avatar'] = self.get_cookie("avatar",avatar)
			msg['nickname'] = self.get_cookie("nickname","神秘人")
			msg['content'] = content
			msg['openid'] = self.get_cookie("openid","")
			coll.insert(msg)
		self.redirect('/form')


class AuthHandler(tornado.web.RequestHandler):
	def get(self):
		CODE = self.get_argument('code', None)
		if CODE:
			APPID = "wxc95158c151a36e16"
			SECRET = "2fcfab3348e281a6dc81fe95e5ee6923"
			self.redirect('http://1.ckwxyy.sinaapp.com/?code='+CODE)

class ApiHandler(tornado.web.RequestHandler):
	def get(self):
		import json
		lastid = self.get_argument('lastid', None)
		coll = self.application.db.msg
		data = coll.find().skip(int(lastid))
		self.render("api.html",
			data = data,
			total = data.count()- int(lastid),)

class HostHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_cookie("nickname", "主持人")
		self.set_cookie("avatar", "http://suosikeji.qiniudn.com/logo-circle.png")
		self.set_cookie("openid", "41255029")
		self.redirect("/form")

class LogHandler(tornado.web.RequestHandler):
	def get(self):
		nickname = self.get_argument('nickname', None)
		avatar = self.get_argument('avatar', None)
		openid = self.get_argument('openid', None)
		self.set_cookie("nickname", nickname)
		self.set_cookie("avatar", avatar)
		self.set_cookie("openid", openid)
		self.redirect("/form")

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()
