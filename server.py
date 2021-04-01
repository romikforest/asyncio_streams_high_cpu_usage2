import asyncio

async def handle_server(reader, writer):
    try:
        while True:
            try:
                data = await reader.read(100)
                addr = writer.get_extra_info('peername')

                print(f"Received message from {addr!r}")

                await asyncio.sleep(0.1) # processing

                print(f"Send response")
                data = b'g' * 100000
                writer.write(data)
                await writer.drain()
            except OSError:
                writer.close()
                raise
    except Exception as e:
        print(type(e), e)
        raise
    finally:
        print("Close the connection")
        writer.close()


async def main():
    server = await asyncio.start_server(handle_server, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
