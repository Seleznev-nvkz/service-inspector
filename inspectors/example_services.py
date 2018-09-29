from textwrap import shorten
from utils.common import InspectorAbstract
from utils.sessions import Session

session = Session("https://google.com", "https://www.youtube.com")


class GoogleCheck(InspectorAbstract):
    interval = 10
    name = 'Google Main Page'

    def check(self):
        response = session.head("https://google.com")
        self.details = {'status': response.status_code, 'headers': response.headers}
        return response.ok


class YoutubeCheck(InspectorAbstract):
    interval = 60
    name = 'Youtube Main Page'

    def check(self):
        response = session.get("https://www.youtube.com")
        self.details = {'status': response.status_code,
                        'content': shorten(response.content.decode(), width=128)}
        return response.ok