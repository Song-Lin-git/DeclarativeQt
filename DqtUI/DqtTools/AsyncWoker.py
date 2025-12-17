import inspect
import math
import time
from functools import partial
from typing import Callable, Any

from PyQt5.QtCore import QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, Run
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import RState
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, isValid, DataBox
from DeclarativeQt.Resource.Strings.RString import RString


class RActor(QThread):
    finished = pyqtSignal(object)
    failed = pyqtSignal()

    def __init__(self, func: Callable, *args: Any, **kwargs: Any):
        super().__init__()
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._running = False
        self._taskEnd = False
        self._result = None
        self.moveToThread(self)

    def broadcast(self):
        if not self._taskEnd or self._running:
            return None
        # noinspection PyUnresolvedReferences
        self.finished.emit(self._result)

    def start(self, *args: QThread.Priority):
        self._taskEnd = False
        return super().start(*args[:1])

    def run(self):
        if self._running:
            return None
        self._running = True
        failed = False
        try:
            self._result = self._func(*self._args, **self._kwargs)
        except Exception as e:
            RString.log(str(e), RString.lgError)
            failed = True
            self._result = None
        time.sleep(0.2)
        if failed:
            # noinspection PyUnresolvedReferences
            self.failed.emit()
        # noinspection PyUnresolvedReferences
        self.finished.emit(self._result)
        self._running = False
        self._taskEnd = True
        return None

    def isRunning(self):
        return self._running

    def isFinished(self):
        return self._taskEnd

    def quit(self):
        self._running = False
        return super().quit()


class RTimer(QThread):
    def __init__(
            self,
            clock: RState[float],
            delayMsec: int = None,
            startTrig: Remember = None,
            restartTrig: Remember = None,
            finishTrig: Remember = None,
    ):
        super().__init__()
        clock = Validate(clock, Remember(0.0))
        clock.setValue(0.0)
        self._qtimer = QTimer(self)
        self.moveToThread(self)
        self._delayMsec = Validate(delayMsec, int(100))
        msecVal = 1 / 1e3
        self._running = False
        if isValid(restartTrig):
            restart = lambda: Run(clock.setValue(0.0), self.start())
            restartTrig.connect(restart, host=self)
        if isValid(startTrig):
            startTrig.connect(partial(self.start), host=self)
        if isValid(finishTrig):
            finishTrig.connect(partial(self.quit), host=self)
        timeMove = lambda a0: a0 + msecVal * self._delayMsec
        # noinspection PyUnresolvedReferences
        self._qtimer.timeout.connect(lambda: clock.updateValue(timeMove))

    def run(self):
        if self._running:
            return None
        self._running = True
        self._qtimer.start(self._delayMsec)
        self.exec_()
        return None

    def isRunning(self):
        return self._running

    def quit(self):
        self._running = False
        self._qtimer.stop()
        return super().quit()


class AsyncWorker(QObject):
    Workings = set()

    class Checker:
        start: float = 4.0
        interval: float = 0.1
        tolerance: float = 2.0

    def __init__(
            self,
            thread: RActor,
            parent: QWidget = None,
            clock: RState[float] = None,
            delayMsec: int = None,
            onFinished: Callable = None,
            autoCheck: bool = True,
    ):
        super().__init__()
        self._worker = thread
        self._parent = parent
        self._worker.setParent(self._parent)
        self._timer = RTimer(clock, delayMsec)
        self._timer.setParent(self._parent)
        self._stopped = False
        # noinspection PyUnresolvedReferences
        self._worker.finished.connect(lambda a0: self.stop(a0))
        self._onFinished = Validate(onFinished, lambda: None)
        self._autoCheck = autoCheck
        ck = self.Checker
        self._startCheck = ck.start
        self._ckclock = Remember(0.0)
        self._tolerance = math.ceil(ck.tolerance / ck.interval)
        self._cktimer = RTimer(self._ckclock, int(1e3 * ck.interval))
        self._ckclock.connect(lambda: self.check(), host=self)
        self._cktimer.setParent(self._parent)
        self._waiting = self._tolerance

    @private
    def check(self):
        if DataBox(
                not self._autoCheck or
                self._ckclock.value() < self._startCheck or
                not self._cktimer.isRunning() or
                self._worker.isRunning() or
                not self._worker.isFinished()
        ).data:
            return None
        self._waiting += -1
        if self._waiting < 0:
            self._worker.broadcast()
            self._waiting = self._tolerance
        return None

    def start(self):
        if self._parent in self.Workings:
            return None
        if isValid(self._parent):
            self.Workings.add(self._parent)
        self._worker.start()
        self._timer.start()
        self._cktimer.start()
        self._stopped = False
        return None

    @private
    def stop(self, workout: Any):
        if self._stopped:
            return None
        self._stopped = True
        self._cktimer.quit()
        self._timer.quit()
        self._worker.quit()
        if self._parent in self.Workings:
            self.Workings.remove(self._parent)
        if len(inspect.signature(self._onFinished).parameters) <= 0:
            self._onFinished()
        else:
            self._onFinished(workout)
        return None
