# coding:utf-8
from flask import Flask, request, render_template, helpers
from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebScoketHandler
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket import WebSocketError
import json
from time import time
# 8282端口
root_path = helpers.get_root_path(__name__) + r"\Web"
app = Flask(__name__, static_url_path="", static_folder="",
            template_folder="", root_path=root_path)
app.debug = True
JOIN_USER = []


class EchoApplication(object):
    """ 说明:
        socket连接时发送数据{"type":"welcome","id":'.$_session_id['id'].'}
        收到json消息时候判断type==>login/update/message
        退出时发送数据：{'type':'closed', 'id':$client_id}
    """

    def __init__(self, ws):
        self.ws = ws

    def run(self):
        self.on_open()
        while True:
            try:
                message = self.ws.receive()
                if message is None:
                    self.on_close(u"用户%s断开连接" % self.session_id)
                    break
            except WebSocketError:
                self.on_close(u"程序异常")
                break
            self.on_message(message)

    def on_open(self):
        """打开连接"""
        # 取时间戳作为用户唯一ID
        self.session_id = str(int(time() * 1000))[-8:]
        JOIN_USER.append(self.ws)

        self.ws.send('{"type": "welcome", "id": %s}' % self.session_id)
        print u"用户上线：%s" % self.session_id
        print u"当前用户:{}".format(
            "|".join([str(id(ws)) for ws in JOIN_USER]))

    def on_message(self, message):
        """发送消息"""
        recv_data = json.loads(message)
        # 更新数据给所有客户端
        for ws in JOIN_USER:
            if recv_data.get("type") == "login":
                return None
            elif recv_data.get("type") == "update":
                ws.send("""{"type":"update",
                    "id":%s,
                    "angle":%s,
                    "momentum":%s,
                    "x":%s,"y":%s,
                    "life":1,
                    "name":"%s",
                    "authorized":false}""" % (
                    self.session_id,
                    recv_data.get("angle"),
                    recv_data.get("momentum"),
                    recv_data.get("x"),
                    recv_data.get("y"),
                    recv_data.get("name", "Guest.%s" % self.session_id)))
            elif recv_data.get("type") == "message":
                ws.send('{"type":"message",\
                    "id":%s,"message":"%s"}' % (
                    self.session_id,
                    recv_data.get("message")))

    def on_close(self, reason):
        """关闭客户端连接"""
        global JOIN_USER
        self.ws.close()
        JOIN_USER = filter(lambda ws: ws != self.ws, JOIN_USER)
        print u"当前用户:{}".format(
            "|".join([str(id(ws)) for ws in JOIN_USER]))
        for ws in JOIN_USER:
            ws.send('{"type":"closed","id":%s}' % self.session_id)
        print reason


@app.route("/")
def index():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        EchoApplication(ws).run()

    return render_template("index.html")


if __name__ == "__main__":
    print "Running on http://127.0.0.1:8282/ (Press CTRL+C to quit)"
    WSGIServer(("127.0.0.1", 8282), app,
               handler_class=WebSocketHandler).serve_forever()
