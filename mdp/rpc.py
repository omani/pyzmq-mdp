# -*- coding: utf-8 -*-

from future.utils import iteritems

import zmq
import json
from zmq.eventloop.ioloop import IOLoop

from worker import MDPWorker
from client import MDPClient, mdp_request


class Server(MDPWorker):

    HB_INTERVAL = 1000
    HB_LIVENESS = 3

    count = 0

    def __init__(self, service=None, name=None, identity=None):
        if service is None:
            service = self

        self._name = name or self._extract_name(service)
        self._methods = self._filter_methods(Server, self, service)

        super(Server, self).__init__(zmq.Context(), "tcp://127.0.0.1:5555", identity)

    def _inspect(self):
        methods = dict((m, f) for m, f in iteritems(self._methods) if not m.startswith('_'))
        detailled_methods = dict((m, dict(args=self._format_args_spec(f._zerorpc_args()), doc=f._zerorpc_doc())) for (m, f) in iteritems(methods))
        return {'name': self._name, 'methods': detailled_methods}

    @staticmethod
    def _extract_name(methods):
        return getattr(methods, '__name__', None) \
            or getattr(type(methods), '__name__', None) \
            or repr(methods)

    @staticmethod
    def _filter_methods(cls, self, methods):
        if isinstance(methods, dict):
            return methods
        server_methods = set(k for k in dir(cls) if not k.startswith('_'))
        return dict((k, getattr(methods, k))
                    for k in dir(methods)
                    if callable(getattr(methods, k)) and
                    not k.startswith('_') and k not in server_methods
                    )

    def on_request(self, msg):
        print "Got a request. Processing..."
        payload = json.loads(msg[0])
        method = payload[0]
        args = payload[1]
        kwargs = payload[2]

        self.count = self.count + 1

        if method not in self._methods:
            raise NameError(method)
        try:
            ret = self._methods[method](*args, **kwargs)
            self.reply(json.dumps(ret))
        except Exception as ex:
            self.reply(json.dumps(str(ex)))
        return

    def run(self):
        IOLoop.instance().start()

    def __destroy__(self):
        self._worker.shutdown()


class Client(MDPClient):

    def __init__(self, worker, *args, **kwargs):
        self.worker_address = worker
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.connect("tcp://127.0.0.1:5555")

    def __call__(self, method, *args, **kwargs):
        payload = json.dumps([method, args, kwargs])
        res = mdp_request(self._socket, self.worker_address, payload, timeout=2.0)

        if res:
            return res[1]
        else:
            return 'Timeout!'

    def on_message(self, msg):
        print "Received:", repr(msg)
        IOLoop.instance().stop()
        return

    def on_timeout(self):
        print 'TIMEOUT!'
        IOLoop.instance().stop()
        return

    def __getattr__(self, method):
        return lambda *args, **kwargs: self(method, *args, **kwargs)

    def __destroy__(self):
        self._socket.close()
        self._context.term()
