# -*- coding: utf-8 -*-

import rpc
import sys

if __name__ == '__main__':
    service = rpc.Client(worker=sys.argv[1])
    print service.hello(msg='world')
