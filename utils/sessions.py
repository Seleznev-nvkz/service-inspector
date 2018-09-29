from collections import OrderedDict
from requests.adapters import HTTPAdapter as BaseAdapter
from requests.sessions import Session as BaseSession


class HTTPAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(pool_connections=2, pool_maxsize=10, max_retries=5, pool_block=False)


class Session(BaseSession):
    def __init__(self, *urls):
        super().__init__()
        self.adapters = OrderedDict()
        for server_url in urls:
            self.mount(server_url, HTTPAdapter())
