# Lapiz is a Tensorboard HTTP Bridge
Lapiz helps you send data to Tensorboard over HTTP (without requiring Tensorflow at the send point): it can then be used from PyTorch for instance. Of course, being a bridge, it adds flexibility at the cost of some latency (not yet measured).

The name Lapiz simply means "crayon" in Spanish, because this cool idea comes from [crayon](https://github.com/torrvision/crayon) client/server library. I decided to rewrite crayon instead of making endless breaking PR because I was not convinced by the API and its server code required quite some rewriting to adopt Tensorboard v1.3.0 HTTP API.


## Overview
The client, a basic Python class that simply requires Python [request](http://docs.python-requests.org/en/latest/) library, sends json data to a server over HTTP. The server, a Flask app, then writes that data to Tensorboard using the Tensorflow `tf.Summary` API.

The server and embarked Tensorboard can be dockerized, which really makes it easy to use Tensorboard from outside Tensorflow ecosystem.

## Usage
On the server instance, run the dockerized server

    docker run -d -p 6006:6006 -p 6007:6007 --name tbhb bosr/tbhb

The first exposed port 6006 is for the browser to connect to Tensorboard web interface, the second 6007 is for lapiz Flask server.

From a client:

    import lapiz as lz
    # connect to lapiz server (6007 by default)
    cl = lz.Client('192.168.78.36:6007')  # or (hostname='192.168.78.36', port=6007)
    ...
    with cl.run('run0,lr=1e-3,lambda=1e-1') as run:
        for _ in range(num_steps):
            # computations here
            ...
            # the global_step starts at 0 by default, but override it with run.step(1)
            run.step()  # now step = 1
            run.add_scalar('accuracy', 1.3e-3)            # numpy types accepted
            run.add_histogram('hidden_weights', weights)  # flatten your weights
            run.add_image('sample', img)
            run.add_audio('audio', waveform)

If the context manager style does not fit you, just don't forget to send and close:

    run = cl.run('run0,lr=1e-3,lambda=1e-1')
    run.step(36)
    run.add_scalar('accuracy', 1e-3)
    run.send()  # send to lapiz server
    run.step(37)
    run.add_scalar('G_loss', 1e-1)
    run.wall_time(11.3)  # arbitrary wall_time
    run.send()
    run.close()  # or del run

The wall time associated to events is taken automatically when `run.save()` is executed, but it can be overwritten with `run.wall_time(time.time())`.

## Format of json messages

