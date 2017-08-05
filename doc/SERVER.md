# The server is build completely inside a docker image.

If you do not have the docker image yet,

    docker pull bosr/lapiz

or build it locally with:

    docker build -t bosr/lapiz:latest .

Then the server can be started with:

    docker run -d -p 6006:6006 -p 6007:6007 --name lapiz bosr/lapiz

Additional arguments can be passed (not yet ready):

- `frontend_refresh` is an optional argument that allows to change the refresh
  rate of tensorboard to the given value (in seconds). Default is 10 seconds.
- `backend_refresh` in an optional argument that allows to change how often the
  tensorflow backend reload the files from disk (in seconds). Default is 0.5
  seconds. Reducing this value too much may make tensorboard unstable.

Finally,

- Tensorboard can then be accessed from a browser at `localhost:6006`.
- The client should be setup to send the data at `localhost:6007`.

## Additional options

This is basic docker, I know, but in case you want to persist logged data outside the container, you can:

    docker run -d -p 6006:6006 -p 6007:6007 --name lapiz -v /path/to/local/persistent/folder:/tmp bosr/lapiz
