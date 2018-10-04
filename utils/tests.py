class MockResponse:
    def __init__(self, content: str, status_code: int):
        self.content = content.encode()
        self.status_code = status_code
        self.ok = status_code < 400
