# wechat_wall
一个简单的微信墙，需要订阅号网页应用授权权限。

#廖总看这里

下面那一部分是我用来做获取权限的，之前学院服务器各种限制不能直接在上面弄，所以就放到`sae`上了。
你改一改就可以用了应该。

```
class VipHandler(tornado.web.RequestHandler):
    def get(self):
        import json
        import urllib
        CODE = self.get_argument('code', None)
        if CODE:
            APPID = "xxxxx"
            SECRET = "xxxx"
            URL = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+APPID+"&secret="+SECRET+"&code="+CODE+"&grant_type=authorization_code"
            result = json.loads(urllib.urlopen(URL).read())
            ACCESS_TOKEN = result["access_token"]
            OPENDID = result["openid"]
    
            URL = "https://api.weixin.qq.com/sns/userinfo?access_token="+ACCESS_TOKEN+"&openid="+OPENDID
            result = json.loads(urllib.urlopen(URL).read())
            nickname = result["nickname"]
            avatar = result["headimgurl"]
            openid = result["openid"]
            
            self.redirect("http://vip.suosikeji.com/log?nickname="+nickname+"&avatar="+avatar+"&openid="+openid)
        else:
            self.write("Hello, world! - Tornado")
```
