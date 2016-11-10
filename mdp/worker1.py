# -*- coding: utf-8 -*-

import rpc


class Methods(object):

    def hello(self, msg):
        return 'Hello {}'.format(msg)

    def helloworld(self):
        return 'Hello world!'


if __name__ == '__main__':
    myserver = rpc.Server(Methods(), identity='worker1')
    myserver.run()
