""" tornado libraries """
import asyncio
import tornado.ioloop
import tornado.web
from tornado.escape import json_decode

""" pywebio library"""
from pywebio.platform.tornado import webio_handler
from pywebio.output import *
from pywebio import STATIC_PATH

""" Other python libraries """
import os
import requests
import json
from dataclasses import dataclass
from pathlib import Path

""" DB """
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine
import apprise as ap

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('APPRISE_TOKEN')
apprise_id = os.getenv('APPRISE_ID')
target = f"tgram://{token}/{apprise_id}"
apobj = ap.Apprise()
apobj.add(target)


class Neko(SQLModel, table=True):
    __tablename__ = "neko_db"
    id: int = Field(primary_key=True)
    name: str
    weight: float
    sex: str


sqlite_file_name = "test.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

db_path = Path(sqlite_file_name)
# print(Path.is_file(db_path))

if Path.is_file(db_path) is True:
    print(f"database already exists: {sqlite_file_name}")
    pass
else:
    print("database does not exist. Hence will be created")
    SQLModel.metadata.create_all(engine)


    def create_db_and_tables():
        SQLModel.metadata.create_all(engine)


    create_db_and_tables()


def fct_neko_data_add(data):
    data = Neko(
        name=data["name"],
        weight=data["weight"],
        sex=data["sex"]
    )
    with Session(engine) as session:
        session.add(data)
        session.commit()


""" Main """
gcd = os.getcwd()
static_path = os.path.join(gcd, 'static')
templates_path = os.path.join(gcd, 'templates')

# print(templates_path)

class MainHandler(tornado.web.RequestHandler):
    """Request handler where requests and responses speak JSON."""

    def get(self):
        # self.write("Hello, world")
        name = self.get_argument('name', 'World')
        self.render('index.html', name=name)

    # def post(self):
    #     r = self.request.body
    #     self.write(r)
    #
    #     request_json = json_decode(self.request.body)
    #     self.write(request_json["username"])
    #     self.write(request_json["password"])
    #
    #     self.write(list(request_json.values())[0])


# https://stackoverflow.com/questions/62292308/alternatives-of-flask-apis-in-tornado-dialogflow-webhook
class Webhook(tornado.web.RequestHandler):

    def post(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            data_input = json.loads(self.request.body)

            # print('data_input:', data_input)
            print('data_input_json.dumps:', json.dumps(data_input, indent=4))

            print(data_input.values())
            data_output = self.webhook_result(data_input)  # get as normal dict, not string

            msg = data_output.get("name")[0]
            print(msg)
            print('data_output:', data_output)

            apobj.notify(
                body=msg,
                title='my notification title'
                # attach=attach
            )

            print('data_output_json.dumps:', json.dumps(data_output, indent=4))

            self.write(data_output)  # it will send as JSON

            # for value in data_input.get("results"):
            #     fct_neko_data_add(value)

        else:
            self.write({'error': 'Wrong Content-Type'})  # it will send as JSON

    def webhook_result(self, data):

        lst = []
        names = []
        weights = []
        sexes = []
        for n in data.get("results"):
            name = n.get("name")
            weight = n.get("weight")
            sex = n.get("sex")
            names.append(name)
            weights.append(weight)
            sexes.append(sex)
            lst.append(n)

        return {
            "name": names,
            "weight": weights,
            "sex": sexes
        }


def task_func() -> None:
    put_markdown("""
        # Year!!!!
        - 1
        - 2
        - 3
    """)


""" mainScript """
settings = dict(
    debug=True,
    static_path=static_path,
    template_path=templates_path
)

handlers = [
    (r"/", MainHandler),
    (r"/webhook", Webhook),
    (r"/tool", webio_handler(task_func))
    # (r'(.*)', web.StaticFileHandler, {'path': static_root})
]

if __name__ == "__main__":
    port = 28080
    application = tornado.web.Application(handlers, **settings)
    application.listen(port=port, address='0.0.0.0')  # run python3 app.py

    # application.listen(port=8080, address='localhost') # run python3 app.py
    print(f"Running: http://127.0.0.1:{port}")
    tornado.ioloop.IOLoop.current().start()
