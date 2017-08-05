# tensorboard --logdir=/tmp/tensorboard --host=localhost --port=6006
# from server folder
# python -m lapiz.boot --port 4800 --tensorboard-folder /tmp/tensorboard

# from client folder
# python minitest.py
import lapiz as lz

c = lz.Client('localhost')  # , port=6007)

with c.run('name0,lr=1e-3') as run:
    for idx in range(1, 10):
        run.step()
        factor = float(idx) * idx
        run.add_scalar('accuracy', 0.8 * factor)
        run.add_scalar('loss', 13415.0 / factor)
        # run.add_histogram('hidden1', weights=range(5))
        # run.add_histogram('hidden1', histo=[range(5), range(5)])
