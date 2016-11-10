# -*- coding: utf-8 -*-

import rpc
import sys

if __name__ == '__main__':
    sys.argv.pop(0)
    service = rpc.Client(worker=sys.argv.pop(0))

    uptime = service.uptime(timeout=10, async=True)
    print service.hello()
    print uptime.get()
