import asyncio
import sys

import bot


async def main():
    tasks = []
    tasks.append(asyncio.create_task(bot.run()))
    for task in tasks:
        print(f"Running task {task.get_coro().__name__}... ")
        await task

if __name__ == '__main__':
    print("Running...")
    print("__name__ is __main__")
    run_args = sys.argv[1:]
    print(f"Run args: {run_args}")
    if '-dev' in run_args:
        ...
    elif '-bot' in run_args:
        print("Running main()...")
        asyncio.run(main())
