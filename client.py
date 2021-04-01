import asyncio
# from connection_pool import ConnectionStrategy, ConnectionPool
from asyncio_connection_pool import ConnectionStrategy, ConnectionPool
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import PlainTextResponse


class Client:

    def __init__(self):
        self.reader, self.writer = None, None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection('127.0.0.1', 8888)

    async def send(self, data):
        self.writer.write(data)
        await self.writer.drain()

    async def read(self, buffersize):
        return await self.recv(buffersize)

    async def recv(self, buffersize):

        bytes_rcvd = 0
        chunks = []

        while bytes_rcvd < buffersize:
            chunk = await self.reader.read(buffersize - bytes_rcvd)
            if chunk == b'':
                raise RuntimeError('Socket connection broken.')
            chunks.append(chunk)
            bytes_rcvd += len(chunk)

        return b''.join(chunks)

    async def close(self):
        print('Close the connection')
        self.writer.close()

    def is_closed(self) -> bool:
        return self.reader and self.writer and not self.writer.is_closing() \
            and not self.writer.get_extra_info('socket').fileno() != -1


class ClientConnectionStrategy(ConnectionStrategy):

    def __init__(self, *args, **kwargs):
        pass

    async def create_client(self):
        client = Client()
        await client.connect()
        return client

    async def make_connection(self):
        return await self.create_client()

    def connection_is_closed(self, conn):
        conn.is_closed()

    def close_connection(self, conn):
        conn.close()


pool = None


def init_pool():
    global pool
    pool = ConnectionPool(strategy=ClientConnectionStrategy(),
                          max_size=200,
                          burst_limit=1000,
                          )


# async def tcp_client():
#     init_pool()
#     async with pool.get_connection() as conn:
#         try:
#             while True:
#                 data = b'g' * 100
#
#                 print(f'Send request')
#                 await conn.send(data)
#
#                 data = await conn.read(100000)
#                 print(f'Response has been received')
#         except Exception as e:
#             print(type(e), e)
#             raise
#         finally:
#             conn.close()
#
#
# asyncio.run(tcp_client())

async def app_endpoint(request):
    async with pool.get_connection() as conn:
        data = b'g' * 100

        print('Send request')
        await conn.send(data)

        data = await conn.read(100000)
        print('Response has been received')
        return PlainTextResponse('Response has been received')


routes = [
    Route('/', endpoint=app_endpoint),
]

async def startup_task():
    init_pool()

app = Starlette(routes=routes,
                on_startup=[startup_task],
                )


def main():
    import uvicorn

    uvicorn.run(app,
                host='127.0.0.1', port=8000,
                )


if __name__ == "__main__":
    main()
