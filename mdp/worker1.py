# -*- coding: utf-8 -*-

import rpc
import gevent


class Methods(object):

    def uptime(self):
        gevent.sleep(3)
        return "Hello"

    def hello(self):
        ok = "LOL"
        return ok


if __name__ == '__main__':
    myserver = rpc.Server(Methods(), identity='worker1')
    myserver.run()
