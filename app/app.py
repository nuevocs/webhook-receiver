import tornado.ioloop
import tornado.web
from pywebio.platform.tornado import webio_handler
from pywebio.output import *
from pywebio import STATIC_PATH
import requests


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def webhook(self):
        if self.request.method == "POST":
            print("Data received from Webhook is: ", requests.json)
            self.write("Webhook received!")
        elif self.request.method == "GET":
            self.write("GET data received.")
        else:
            pass


def task_func() -> None:
    put_markdown("""
        # Year!!!!
        - 1
        - 2
        - 3
    """)


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/tool", webio_handler(task_func)),  # `task_func` is PyWebIO task function
    ])
    application.listen(port=8080, address='0.0.0.0') # run python3 app.py

    # application.listen(port=8080, address='localhost') # run python3 app.py

    tornado.ioloop.IOLoop.current().start()