import argparse
import asyncio

from tornado_server import make_app



async def amain():
    parser = argparse.ArgumentParser(description="Start Tornado server with a specified port")
    parser.add_argument("--port", type=int, default=8888, help="Port number to run the server")
    args = parser.parse_args()

    app = make_app()
    app.listen(args.port,"0.0.0.0")
    print(f"Server is served at http://anywhere:{args.port}")
    await asyncio.Event().wait()


def main():
    asyncio.run(amain())

if __name__ == '__main__':
    main()