# Lapiz is a Tensorboard HTTP Bridge
Lapiz helps you send data to Tensorboard over HTTP (without requiring Tensorflow at the send point): it can then be used from PyTorch for instance. Of course, being a bridge, it adds flexibility at the cost of some latency (not yet measured).

The name Lapiz simply means "crayon" in Spanish, because this cool idea comes from [crayon](https://github.com/torrvision/crayon) client/server library. I decided to rewrite crayon instead of making endless breaking PR because I was not convinced by the API or naming ("experiment" vs "run", etc) and its server code required quite some rewriting to adopt Tensorboard v1.3.0 HTTP API.


## Overview
The client, a basic Python class that simply requires Python [request](http://docs.python-requests.org/en/latest/) library, sends json data to a server over HTTP. The server, a Flask app, then writes that data to Tensorboard using the Tensorflow `tf.Summary` API.

The server and embarked Tensorboard can be dockerized, which really makes it easy to use Tensorboard from outside of the Tensorflow ecosystem.


## Quickstart
### Server-side
On the server instance, run the dockerized server

    docker run -d -p 6006:6006 -p 6007:6007 --name lapiz bosr/lapiz

The first exposed port 6006 is for the browser to connect to Tensorboard web interface, the second 6007 is for lapiz Flask server.

### Client-side
In your project virtualenv, install the [lapiz-client](https://github.com/bosr/lapiz-client) python library:

    pip install lapiz-client  # available on Pypi

From a client:

    import lapiz as lz

    cl = lz.Client('192.168.78.36', port=6007)  # check connection to lapiz server (6007 by default)

    with cl.run('run0,lr=1e-3,lambda=1e-1') as run:
        for _ in range(num_steps):

            # ...

            # the global_step starts at 0 by default, but override it with run.step(1)
            run.step()  # now step is 1

            run.add_scalar('accuracy', 1.3e-3)            # numpy types accepted
            run.add_histogram('hidden_weights', weights)  # flatten your weights
            run.add_image('sample', img)
            run.add_audio('audio', waveform)

            # run.save()  # not needed unless you cannot wait for the next run.step()

Each time the `run.step()` instruction is executed, the client saves all
unsaved summaries, if any. You can save those summaries as early as you want
with `run.save()`. The context manager makes it sure unsaved summaries will be
saved at exit.

If the context manager style adopted by `run` does not fit you, use it directly
but just don't forget to save and close:

    run = cl.run('run0,lr=1e-3,lambda=1e-1')
    run.step(36)
    run.add_scalar('accuracy', 1e-3)
    run.save()  # send to lapiz server
    run.step(37)
    run.add_scalar('G_loss', 1e-1)
    run.wall_time(11.3)  # arbitrary wall_time
    run.save()
    run.close()  # or del run

The wall time associated to events is taken automatically when `run.save()` is
executed, but it can be overwritten with `run.wall_time(time.time())`.

## Additional doc

- Format of json messages: [doc/JSON.md](doc/JSON.md)
- API specs for the Flask server (not yet updated): [doc/specs.md](doc/specs.md)
- More server-side options: [doc/SERVER.md](doc/SERVER.md)
- `lapiz-client` docs: https://github.com/bosr/lapiz-client
