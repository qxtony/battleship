import asyncio

from battleship.config import server
from battleship.instance import game
from battleship.sockets.accept_messages import accept_messages

from loguru import logger


async def main():
    loop = asyncio.get_running_loop()

    await asyncio.gather(
        loop.run_in_executor(None, logger.catch(game.init_data)),
        loop.run_in_executor(None, logger.catch(server.start)),
        loop.run_in_executor(None, logger.catch(accept_messages)),
    )


if __name__ == "__main__":
    asyncio.run(main())
