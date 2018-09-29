import inspectors

from pkgutil import iter_modules
from report.telegram import TelegramReporter

from utils.common import InfiniteTimer, InspectorBuilder


class MainKeeper:
    """
    Unite all inspectors and observe for them
    example of data
    {'Example Services':
         {'Google Main Page': (True, {'some': 'details'}),
          'Youtube Main Page': (True, {'some': 'details'})}
    }
    """
    reporters = ()

    def __init__(self):
        modules_info = list(iter_modules(inspectors.__path__))

        self.projects = [InspectorBuilder(module_info) for module_info in modules_info]
        self._launched = False
        self.reporters = (TelegramReporter(), )
        self.reporters_thread = InfiniteTimer(60, self.status_check, name='reporters')

    def status_check(self):
        data = {project.name: project.data for project in self.projects if not project}
        if data:
            for reporter in self.reporters:
                reporter.send_alarm(data=data)

    def run(self):
        if not self._launched:
            for project in self.projects:
                project.run()
            self.reporters_thread.start()
            self._launched = True

    def stop(self):
        if self._launched:
            for project in self.projects:
                project.stop()
            self.reporters_thread.stop()
            self._launched = False

    @property
    def is_launched(self):
        return self._launched

    @property
    def data(self):
        assert self._launched, 'Not launched inspectors'
        return {project.name: project.data for project in self.projects}

    @property
    def ok(self):
        return all(self.projects)
