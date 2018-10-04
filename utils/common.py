from pkgutil import ModuleInfo
from inspect import getmembers
from threading import Timer, Event, Thread


class InfiniteTimer(Timer):
    """
    t = Timer(30.0, f, name, args=None, kwargs=None)
            t.start()
            t.stop()     # stop the timer's action if it's still waiting
    """
    def __init__(self, interval, target, name, *args, **kwargs):
        Thread.__init__(self, name=name, daemon=True)
        self.interval = interval
        self.target = target
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = Event()
        self._launched = Event()

    def stop(self):
        self.finished.set()

    def start(self):
        if self._launched.is_set():
            self.finished.clear()
        else:
            super().start()
            self._launched.set()

    def run(self):
        while not self.finished.is_set():
            self.target(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


class InspectorAbstract:
    """ Starting thread with check by set interval
        interval - required, value in seconds to run 'check' method
        name - required, name of Inspector to view
        details - not required, will show extra data if set
    """
    interval = None
    name = None
    details = None

    def __init__(self):
        self.result = True
        class_name = type(self).__name__
        assert self.name, f'Set name for {class_name}'
        assert self.interval, f'Set interval for {class_name}'
        self.details = {}
        self.thread = InfiniteTimer(int(self.interval), self._run, name=f'hawkeye thread {class_name}')

    def run(self):
        self.thread.start()

    def _run(self):
        """ Should be run into thread """
        self.result = self.check()

    def stop(self):
        self.thread.stop()

    def check(self):
        """ Check service and save to result """
        raise NotImplementedError()

    def __bool__(self):
        """ Health of service without details;
            may be override - by default true/false """
        return self.result

    def __repr__(self):
        return f'{self.name} - {self.result}'

    def set_details_from_response(self, response):
        self.details = {'status': response.status_code, 'body': response.content.decode()}


class InspectorBuilder:
    """ Unite all inspectors for project"""

    def __init__(self, module_info: ModuleInfo):
        def check_member(member):
            return isinstance(member, type) and InspectorAbstract in member.__mro__ and member != InspectorAbstract

        self.name = module_info.name.replace('_', ' ').capitalize()
        self.instances = []
        module = module_info.module_finder.find_module(module_info.name).load_module()
        for member in getmembers(module, check_member):
            try:
                self.instances.append(member[1]())
            except AssertionError as e:
                print(str(e))
        self._launched = False

    def run(self):
        if not self._launched:
            for instance in self.instances:
                instance.run()
            self._launched = True

    def stop(self):
        if self._launched:
            for instance in self.instances:
                instance.stop()
            self._launched = False

    @property
    def data(self):
        assert self._launched, 'Not launched inspectors'
        return {i.name: (bool(i), i.details) for i in self.instances}

    def __bool__(self):
        return all(self.instances)

    def __repr__(self):
        return f'{self.name}: {self.instances}'

    def __len__(self):
        return len(self.instances)
