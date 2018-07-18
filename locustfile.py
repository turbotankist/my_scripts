
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from locust import HttpLocust, TaskSet, task
from locust.events import request_success
from websocket import create_connection

import json
import uuid
import time, sys
import gevent
import six

# def login(l):
#     l.client.post("/login", {"username":"al@45545.com", "password":"454"})
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))

def index(l):
    l.client.get("/")

def privacy(l):
   # l.client.get("/privacy-policy/")
    l.client.get("/privacy-policy")

def contact(l):
   # l.client.get("/contact-us")
    l.client.get("/contact-us")

def terms(l):
    #l.client.get("/terms-and-conditions")
    l.client.get("/checkout")


class UserBehavior(TaskSet):
    # def on_start(self):
    #     self.client.verify = False
        
    tasks = {index: 1, privacy: 2, contact: 1, terms: 1}

    # def on_start(self):
    #     self.user_id = six.text_type(uuid.uuid4())
    #     ws = create_connection('wss://address.com/rts/?EIO=3&transport=polling')
    #     self.ws = ws

    #     def _receive():
    #         while True:
    #             res = ws.recv()
    #             data = json.loads(res)
    #             sys.stdout.write("WS DATA: ",data, "WS RES: ",res)
    #             end_at = time.time()
    #             response_time = int((end_at - data['start_at']) * 1000000)
    #             request_success.fire(
    #                 request_type='WebSocket Recv',
    #                 name='/rts/?EIO=3&transport=websocket&uid=',
    #                 response_time=response_time,
    #                 response_length=len(res),
    #             )

    #     gevent.spawn(_receive)

    # def on_quit(self):
    #     self.ws.close()

    # @task
    # def sent(self):
    #     start_at = time.time()
    #     body = json.dumps(["message", {"payload": {"email": "hgj.com", "passw": "ytyt"}, "type": "AUTH"}])
    #     self.ws.send(body)
    #     request_success.fire(
    #         request_type='WebSocket Sent',
    #         name='/rts/?EIO=3&transport=websocket&uid=',
    #         response_time=int((time.time() - start_at) * 1000000),
    #         response_length=len(body),
    #     )


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000