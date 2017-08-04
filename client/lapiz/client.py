"""
Lapiz client

"""
from __future__ import print_function

import requests
from . import __version__
from .run import Run


class Client(object):
    def __init__(self, hostname, port=6007):
        self.hostname = hostname
        self.port = int(port)
        self._runs = []  # holds existing runs

        if (self.hostname.startswith("http://") or
                self.hostname.startswith("https://")):
            raise ValueError('Hostname should be formatted as an ip: x.x.x.x')
        self.url = "http://{}:{}".format(self.hostname, self.port)

        check_health(self.url)  # will throw if server is not connected


    def close(self):
        for r in self._runs:
            if r.summaries:
                print('Warning: run "{}" has unsaved content'.format(r.name))


    def run(self, name, step=0):
        r = Run(name, client=self, step=step)
        self._runs.append(r)
        return r


    def send_payload(self, runname, payload):
        url = self.url + '/data/run/' + runname + '/summary'
        requests.post(url, json=payload)


def check_health(url):
    url += '/health'

    # check server is working (not only up).
    try:
        r = requests.get(url)
        if not r.ok:
            raise RuntimeError("Something went wrong! Server sent: {}.".format(r.text))
    except requests.ConnectionError:
        msg = "The server at {} does not appear to be up! Please check manually"
        raise ValueError(msg.format(url))

    # compare server and client versions
    server_version = r.json().get('version')
    server_major_minor_version = '.'.join(server_version.split('.')[:2])  # '0.5.1' -> '0.5'
    client_major_minor_version = '.'.join(__version__.split('.')[:2])  # '0.5.2' -> '0.5'

    if server_major_minor_version != client_major_minor_version:
        msg = "Incompatible client ({}) / server ({}) versions"
        raise RuntimeError(msg.format(__version__, server_version))
