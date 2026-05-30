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


async def fetch(url: str) -> str:
    # TODO: mock a network delay with asyncio.sleep (random 0.1–0.5s)
    # then return a result string like f"Response from {url}"
    pass


async def fetch_all(urls: list[str]) -> list[str]:
    # TODO: use asyncio.gather to run all fetches concurrently
    pass


async def fetch_sequential(urls: list[str]) -> list[str]:
    # TODO: fetch each URL one at a time (no gather) to show the difference
    pass


if __name__ == "__main__":
    print("=== Concurrent ===")
    # TODO: time and run fetch_all

    print("\n=== Sequential ===")
    # TODO: time and run fetch_sequential
