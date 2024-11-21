import asyncio

import bot


async def main():
    tasks = []
    tasks.append(asyncio.create_task(bot.run()))
    for task in tasks:
        print(f"Running task {task.get_coro().__name__}... ", end='')
        await task

if __name__ == '__main__':
    print("Running...")
    print("__name__ is __main__")
    print("Running main()...")
    asyncio.run(main())
