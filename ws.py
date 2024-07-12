import websocket
import json
import logging
import threading

from variable import variable

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
logger=logging.getLogger('WebSocket')
class WS(object):
    api_url=None
    token=None
    status=False
    wsc=None
    def __init__(self,api_url=None,token=None):
        self.api_url=api_url
        self.token=token

    def on_message(self,ws,message):
        if variable.main_stop:
            self.wsc.close()
        logger.debug(f"接收到消息: {message}")
        threading.Thread(target=variable.processer.processMessage,args=(message,)).start()

    def on_error(self,ws,error):
        logger.error(f"出现错误: {error}")

    def on_close(self,ws,close_status_code,close_msg):
        logger.info(f"WebSocket连接已关闭")
        logger.info(f"关闭状态码: {close_status_code}")
        logger.info(f"关闭信息: {close_msg}")
        self.status=False

    def on_open(self,ws):
        logger.info(f"WebSocket连接已建立")
        self.status=True

    def start(self):
        header=dict()
        if (not self.api_url is None) and (not variable.bot_id is None):
            if self.token is None:
                header={"bot_id": str(variable.bot_id)}
            else:
                header={"bot_id": str(variable.bot_id),"Authorization": "Bearer "+self.token}
            self.wsc=websocket.WebSocketApp(self.api_url,header=header,
                                           on_open=self.on_open,
                                           on_message=self.on_message,
                                           on_error=self.on_error,
                                           on_close=self.on_close)
            self.wsc.run_forever()
    def send(self,msg):
        self.wsc.send(msg)

    def close(self):
        self.wsc.close()

    def get_status(self):
        return self.status
