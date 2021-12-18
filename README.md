# golem-bulk-image-handler
Generates images in bulk from image inputs.

## Running

Follow the [quick primer example](https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development) to start your yagna daemon or run the following commands in the folder:
```
yagna service run
set YAGNA_APPKEY=<YOUR_APPKEY>
yagna payment init --sender
py main.py
```

## About

This project is based off the [Task Example 0: Hello World!](https://handbook.golem.network/requestor-tutorials/task-processing-development/task-example-0-hello) tutorial and modified to include most of what's needed for a normal Python application to run on Golem.

Instead of building a new Dockerfile everytime we change input or Python file, we upload our input in [line 15](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L15), and our Python script in [line 23](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L23) and run the script in [line 24](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L24).

To further optimize the amount of times we change the Dockerfile, we also create our folders at [line 18-20](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L18). This is instead of adding more text after the VOLUME in the Dockerfile.

Furthermore, to get our result, we download our zipped output in [line 27](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L27). This is instead of only doing what the initial example goes through, which just [prints the console output](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L43).

If you want to recreate it yourself or take inspiration, it's important to take note that the Dockerfile in this project looks like [this](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/Dockerfile) and includes Python module installations, a different base image, and a few packages unlike the original example's [Dockerfile](https://github.com/golemfactory/yapapi/blob/master/examples/hello-world/Dockerfile) which has almost nothing.

When you add your own packages similar to the `RUN pip install <MODULE_NAME>`, it's important that you understand a bit of docker. [Here](https://handbook.golem.network/requestor-tutorials/vm-runtime/creating-a-docker-image) are the official docs on how to create and push a Docker image to Golem. Generally, I just had to run these commands:
```
cd <DIRECTORY_NAME>
docker build -t <PROJECT_NAME>:latest .
python -m gvmkit_build <PROJECT_NAME>:latest
python -m gvmkit_build <PROJECT_NAME>:latest --push
```
Please note that normally it will be `gvmkit-build` and not `gvmkit_build` in the above, but something got messed up in my installation. After running these commands, you will get an output similar to `7a9942463f9d285ae4a36739484140fcccc1c6c0181e3a33fd9bd990`. This is something that you will need to swap out for the `image_hash="",´ part in [line 36](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L36) so that providers can know what to pre-install before running your application.

If you take a look at the Python script that is being run on providers, [providers.py](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/provider.py), you can see some weird things about it that normally isn't in a Python script. Instead of file-paths that looks like this `input/input.jpg`, we must use file-paths similar to `/golem/input/input.jpg`, as this is the prefix defined in the [Dockerfile at line 6](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/Dockerfile#L6), and normal file-paths added ontop of that. You can see examples of these file-paths at [line 5](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/provider.py#L5), [line 13](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/provider.py#L13), [line 22](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/provider.py#L22), [line 32](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/provider.py#L32), and [line 36](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/provider.py#L36).

Generally speaking, [main.py](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py) deals with the yagna daemon and communication, as well as what's being ran on the provider - which is defined from [line 12](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L12) to [line 27](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L27), and also the image necessary to run the app, which is listed on [line 36](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/main.py#L36). [provider.py](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/provider.py) is uploaded to the provider and ran there, and is not ran at all on the requestor/your PC. The [Dockerfile](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/Dockerfile) lets the provider know what's necessary to install, download, and run, for the application to run. [input/input.jpg](https://github.com/figurestudios/golem-bulk-image-handler/blob/main/input/input.jpg) gets uploaded and processed on the provider, and then an output file will magically appear once it's ran.
