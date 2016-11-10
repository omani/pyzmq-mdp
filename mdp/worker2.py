# -*- coding: utf-8 -*-

import rpc


class Methods(object):

    def uptime(self, msg):
        return "Hello " + msg

    def hello(self):
        ok = "LOL"
        return ok


if __name__ == '__main__':
    myserver = rpc.Server(Methods(), identity='worker2')
    myserver.run()
