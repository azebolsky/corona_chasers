import os

import postgres
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

postgres_url = os.getenv('POSTGRES_URL', 'postgres://localhost:5432')

conn = postgres.from_url(postgres_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()