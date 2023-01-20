import asyncio

from battleship.config import server
from battleship.instance import game
from battleship.sockets.accept_messages import accept_messages


async def main():
    loop = asyncio.get_running_loop()

    await asyncio.gather(
        loop.run_in_executor(None, game.init_data),
        loop.run_in_executor(None, server.start),
        loop.run_in_executor(None, accept_messages),
    )


if __name__ == "__main__":
    asyncio.run(main())
