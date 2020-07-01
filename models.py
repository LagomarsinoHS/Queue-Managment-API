import os
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
db = SQLAlchemy()


class Queue:

    def __init__(self):
        self.account_sid = os.environ.get("ACCOUNT_ID")
        self.auth_token = os.environ.get("AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)

        self._queue = ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5"]
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'

    def enqueue(self, item):
        message = self.client.messages \
            .create(
                body=f"Hola {item} faltan {self.size()-1} y serás atendido!",
                from_=os.environ.get("PHONE"),
                to="+56991650806"
            )

    def dequeue(self):
        if self._mode == "FIFO":
            if len(self.get_queue()) == 1:
                message = self.client.messages \
                    .create(
                        body=f"Hola {self._queue[0]}. Es tu turno",
                        from_=os.environ.get("PHONE"),
                        to="+56991650806"
                    )
                self._queue.pop()
            else:
                self._queue.pop(0)

        if self._mode == "LIFO":
            if len(self.get_queue()) == 1:
                message = self.client.messages \
                    .create(
                        body=f"Hola {self._queue[0]}. Es tu turno",
                        from_=os.environ.get("PHONE"),
                        to="+56991650806"
                    )
                self._queue.pop(0)
            else:
                del self._queue[-1]

    def get_queue(self):
        return self._queue

    def size(self):
        return len(self._queue)
