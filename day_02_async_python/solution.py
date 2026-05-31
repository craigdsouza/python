import asyncio
import random
import time

# Challenge: Write an async function fetch_all(urls: list[str]) that:
# - Uses asyncio.gather with asyncio.sleep as a mock for HTTP delay (random 0.1–0.5s per URL)
# - Prints results in completion order
# - Prints total elapsed time
# - Also write a sequential version to show why async is faster

URLS = [
    "https://api.example.com/users",
    "https://api.example.com/posts",
    "https://api.example.com/comments",
    "https://api.example.com/photos",
    "https://api.example.com/todos",
]

async def random_fetch(url:str) -> str:
    interval = (random.randint(10,50))/100
    await asyncio.sleep(interval)
    return (f"Response from {url}")


async def fetch(url: str) -> str:
    # TODO: mock a network delay with asyncio.sleep (random 0.1–0.5s)
    # then return a result string like f"Response from {url}"
    try:
        result = await asyncio.wait_for(random_fetch(url),timeout=0.4)
        return result
    except asyncio.TimeoutError:
        return(f"TIMEOUT: {url}")

async def fetch_all(urls: list[str]) -> list[str]:
    # TODO: use asyncio.gather to run all fetches concurrently
    coroutines = [fetch(url) for url in urls]
    return await asyncio.gather(*coroutines)

async def fetch_all_immediately(urls: list[str]) -> list[str]:
    tasks =  [asyncio.create_task(fetch(url)) for url in urls]
    return [await t for t in tasks]

async def fetch_sequential(urls: list[str]) -> list[str]:
    # TODO: fetch each URL one at a time (no gather) to show the difference
    return [await fetch(url) for url in urls]

async def producer(queue: asyncio.Queue):
    for url in URLS:
        await queue.put(url)
        # print(f"Produced {url}")
    await queue.put(None)

async def worker(queue: asyncio.Queue):
    result = []
    while True:
        item = await queue.get()
        if item is None:
            break
        # print(f"Consumed {item}")
        result.append(await fetch(item))
        queue.task_done()
    return result

async def run_queue()-> list[str]:
    queue = asyncio.Queue()
    return await asyncio.gather(producer(queue),worker(queue))

if __name__ == "__main__":
    print("\n=== Concurrent (asyncio.gather) ===")
    # TODO: time and run fetch_all
    start = time.time()
    results = asyncio.run(fetch_all(URLS))
    print(type(results),len(results))
    for s in results:
        print(s)
    end = time.time()
    duration = end - start
    print(f"Time for parallel with gather:{duration} seconds")

    print("\n=== Concurrent (asyncio.create_task) ===")
    start = time.time()
    results = asyncio.run(fetch_all_immediately(URLS))
    print(type(results),len(results))
    for s in results:
        print(s)
    end = time.time()
    duration = end - start
    print(f"Time for parallel with create_task:{duration} seconds")

    print("\n=== Concurrent (asyncio.Queue) ===")
    start = time.time()
    results = asyncio.run(run_queue())
    print(type(results[1]),len(results[1]))
    for s in results[1]:
        print(s)
    end = time.time()
    duration = end - start
    print(f"Time for parallel with Queue:{duration} seconds")

    print("\n=== Sequential ===")
    # TODO: time and run fetch_sequential
    start = time.time()
    results = asyncio.run(fetch_sequential(URLS))
    print(type(results),len(results))
    for s in results:
        print(s)
    end = time.time()
    duration = end - start
    print(f"Time for sequential:{duration} seconds")

