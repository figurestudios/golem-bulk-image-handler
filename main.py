#!/usr/bin/env python3
import asyncio
from typing import AsyncIterable

from yapapi import Golem, Task, WorkContext
from yapapi.log import enable_default_logger
from yapapi.payload import vm


async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        script = context.new_script()

        # upload our input image
        script.upload_file("./input/input.jpg", "/golem/input/input.jpg")

        # generate our folders
        script.run("/bin/sh", "-c", 'mkdir -p "/golem/input/output/rotation/"')
        script.run("/bin/sh", "-c", 'mkdir -p /golem/input/output/filter/')
        script.run("/bin/sh", "-c", 'mkdir -p /golem/input/output/resize/')

        # upload and run .provider.py on the provider
        script.upload_file("provider.py", "/golem/input/provider.py")
        future_result = script.run("/usr/bin/python3", "/golem/input/provider.py")

        # download the target.7z file from our output, this is our result
        script.download_file("/golem/input/target.7z", "./output/target.7z")

        yield script

        task.accept_result(result=await future_result)


async def main():
    package = await vm.repo(
        image_hash="34b9aa998ae412a3901fe15029a3ee5b60b91bd306192d414dffe862",
    )

    tasks = [Task(data=None)]

    async with Golem(budget=1.0, subnet_tag="devnet-beta") as golem:
        async for completed in golem.execute_tasks(worker, tasks, payload=package):
            print(completed.result.stdout)


if __name__ == "__main__":
    enable_default_logger(log_file="out.log")

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)