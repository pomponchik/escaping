import sys

from exception_escaping.proxy_module import ProxyModule


sys.modules[__name__].__class__ = ProxyModule
