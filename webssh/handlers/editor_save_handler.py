from webssh.handler import MixinHandler
from tornado.web import RequestHandler
from tornado.escape import json_decode
from webssh.worker import connected_workers
from tornado.log import app_log

class EditorSaveHandler(MixinHandler, RequestHandler):
    def post(self):
        json_data = json_decode(self.request.body)

        worker = connected_workers[json_data['id']]
        sin, _, _ = worker.ssh.exec_command("tee source.txt")
        sin.write(json_data['content'])

        self.write({
            "msg": "save OK.",
            "content": json_data['content'] # for debug
        })
