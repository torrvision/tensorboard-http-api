"""
Run related data to be collected and sent

"""
from __future__ import print_function

import time
from collections import namedtuple


ScalarSummary = namedtuple('ScalarSummary', ['tag', 'value'])
HistogramSummary = namedtuple('HistogramSummary', ['tag', 'weights', 'histogram'])


class Run(object):
    """
    Run allow summaries to be defined and sent to the server.

    Summaries contain values, histograms, images and/or audio.

    Args:
        name (str): name of the run, can include commas, but avoid non-ascii please
                    (because Tensorboard is said not to like it)

        client (Client): Client object to use for connection

    Note:
        Run not be instantiated without a client, it normally is
        instantiated by the `run` method of the class `Client`.

    """
    def __init__(self, name='run0', client=None, step=0):
        self.name = name
        if not client:
            raise RuntimeError('Missing Client object')
        self._client = client

        # summary holding members
        self._step = step
        self._wall_time = None  # will be taken as time.time() on save()
        self.summaries = []


    def close(self):
        self.save()


    def save(self):
        if not self.summaries:
            return False  # indicates whether save occured or not

        if not self._wall_time:
            self._wall_time = time.time()

        # job to be done
        payload = {
            'wall_time': self._wall_time,
            'step': self._step,
            'summaries': map(serialize, self.summaries)
        }

        self._client.send_payload(self.name, payload)

        self._wall_time = None  # will be taken as time.time on next save()
        self.summaries[:] = []  # clear in place
        return True


    def step(self, new_step=None):
        """
        If you do not provide a new_step, global step will be incremented.

        """
        # save existing summaries
        save_status = self.save() if self.summaries else False

        if new_step is None:
            self._step += 1
        else:
            self._step = new_step

        return save_status


    def wall_time(self, wall_time):
        self._wall_time = wall_time


    # summary interface


    def add_summary(self, summary):
        self.summaries.append(summary)


    def add_scalar(self, tag='accuracy', value=None):
        if value is None:
            raise ValueError('Missing value')
        self.summaries.append(ScalarSummary(tag, value))


    def add_histogram(self, tag='weights', weights=None, histo=None):
        """
        Append a Histogram summary.

        Note:
            weights and histo arguments are mutually exclusive.
            Weights correspond to tensor weights: they will be converted
            to an actual histogram on the server before being passed to Tensorboard. Histo corresponds
            to an existing histogram which will be passed as such to Tensorboard.

        """
        if (weights and histo) or (not weights and not histo):  # mutually exclusive options
            raise ValueError('Wrong usage of add_histogram: weights and histo are mutually exclusive options')
        self.summaries.append(HistogramSummary(tag, weights, histo))


    # context manager interface
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.save()


def serialize(summary):
    if isinstance(summary, ScalarSummary):
        return dict(tag=summary.tag, value=summary.value, type='scalar')
    elif isinstance(summary, HistogramSummary):
        return dict(tag=summary.tag, weights=summary.weights, histo=summary.histogram, type='histogram')
    else:
        raise ValueError('Unsupported summary')
