import asyncio
import sys

import bot
import managers


async def main():
    tasks = []
    tasks.append(asyncio.create_task(bot.run()))
    for task in tasks:
        print(f"Running task {task.get_coro().__name__}... ", end='')
        await task

if __name__ == '__main__':
    print("Running...")
    print("__name__ is __main__")
    run_args = sys.argv
    print(f"Run args: {run_args}")
    if '-dev' in run_args:
        endp = managers.BotMenuNavigationManager.get_menu_endpoint('menu/articles')
        print(endp)
    elif '-bot' in run_args:
        print("Running main()...")
        asyncio.run(main())


