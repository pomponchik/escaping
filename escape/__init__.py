import sys

from escape.proxy_module import ProxyModule as ProxyModule


sys.modules[__name__].__class__ = ProxyModule
