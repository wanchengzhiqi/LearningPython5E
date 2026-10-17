# Async examples.  Per the book, copy/paste, stub out with """, or run as a whole.

import time, asyncio


def now():
    return time.strftime('[%H:%M:%S]')         # Local time, as hour:minute:second


print('1-----------------------------------------------------')


def producer(label):
    time.sleep(2)                              # Pause for two seconds: blocking
    return f'All done, {label}, {now()}'       # And return a result


def main():
    print('Start =>', now())
    print(producer(f'serial task 1'))          # Run three steps in sequence
    print(producer(f'serial task 2'))          # Waiting for each one to finish
    print(producer(f'serial task 3'))          # Before doing anything else
    print('Stop  =>', now())


main()

print('2-----------------------------------------------------')


async def producer(label):                     # await requires async
    await asyncio.sleep(2)                     # Call nonblocking/awaitable sleep
    return f'All done, {label}, {now()}'       # Result of await expression


async def main():
    print('Start =>', now())
    task1 = asyncio.create_task(producer(f'async task 1'))
    task2 = asyncio.create_task(producer(f'async task 2'))
    task3 = asyncio.create_task(producer(f'async task 3'))
    print(await task1)
    print(await task2)
    print(await task3)                         # Wait for tasks to finish
    print('Stop  =>', now())


asyncio.run(main())                            # Start event-loop schedule

print('3-----------------------------------------------------')


async def producer(label):
    await asyncio.sleep(2)
    return f'All done, {label}, {now()}'


async def main(trace=False):
    print('Start =>', now())
    counts, tasks = 0, []
    for i in range(3):
        tasks.append(asyncio.create_task(producer(f'async task {i+1}')))
    for task in tasks:
        if trace:
            counts += 1
            print(f"[TRACE TIME]\t{counts}  {now()}")
        print(await task)
    print('Stop  at', now())


asyncio.run(main(trace=True))

print('4-----------------------------------------------------')


async def producer(label):
    await asyncio.sleep(2)
    return f'All done, {label}, {now()}'


async def main(trace=False):
    print('Start =>', now())
    counts, coros = 0, [producer(f'async task {i}') for i in range(1, 4)]
    for nextdone in asyncio.as_completed(coros):
        if trace:
            counts += 1
            print(f"[TRACE TIME]\t{nextdone}\t{counts}  {now()}")
        print(await nextdone)
    print('Stop  at', now())


asyncio.run(main(trace=True))

print('5-----------------------------------------------------')


async def producer(label):
    await asyncio.sleep(2)
    return f'All done, {label}, {now()}'


async def main():
    print('Start =>', now())
    coro1 = producer(f'async task 1')
    coro2 = producer(f'async task 2')
    coro3 = producer(f'async task 3')
    results = await asyncio.gather(coro1, coro2, coro3)
    print(results)
    print('Stop  at', now())


asyncio.run(main())

print('6-----------------------------------------------------')


async def producer(label):
    await asyncio.sleep(2)
    return f'All done, {label}, {now()}'


async def main():
    print('Start =>', now())
    print(await asyncio.gather(*[producer(f'async task {i+1}') for i in range(3)]))
    print('Stop  at', now())


asyncio.run(main())

print('7-----------------------------------------------------')


async def producer(label):
    await asyncio.sleep(2)
    return f'All done, {label}, {now()}'


async def main():
    print('Start =>', now())
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(producer(f'async task {i+1}')) for i in range(3)]
    for task in tasks:
        print(task.result())
    print('Stop  at', now())


asyncio.run(main())

print('8-----------------------------------------------------')


async def producer(label):
    for i in range(1, 4):
        await asyncio.sleep(2)
        yield f'All done, {label} {i}, {now()}'


async def main():
    print('Start =>', now())
    async for reply in producer('async task'):
        print(reply)
    print('Stop  at', now())


asyncio.run(main())
