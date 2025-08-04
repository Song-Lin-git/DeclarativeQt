from functools import partial
from typing import Callable

from PyQt5.QtCore import QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, Run
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import RState
from DeclarativeQt.Resource.Grammars.RGrammar import GList, Validate, isValid


class RActor(QThread):
    finished = pyqtSignal(list)

    def __init__(self, func: Callable, *args, **kwargs):
        super().__init__()
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._running = False

    def run(self):
        if self._running:
            return None
        self._running = True
        result = self._func(*self._args, **self._kwargs)
        # noinspection PyUnresolvedReferences
        self.finished.emit(GList(result))
        return None

    def quit(self):
        self._running = False
        return super().quit()


class RTimer(QThread):
    def __init__(
            self,
            timer: RState[float],
            delayMsec: int = None,
            startTrig: Remember = None,
            restartTrig: Remember = None,
            finishTrig: Remember = None,
    ):
        super().__init__()
        timer = Validate(timer, Remember(0.0))
        self._qtimer = QTimer(self)
        self.moveToThread(self)
        self._delayMsec = Validate(delayMsec, int(100))
        msecVal = 1 / 1000.0
        self._running = False
        if isValid(restartTrig):
            restartTrig.connect(lambda: Run(timer.setValue(0.0), self.start()), host=self)
        if isValid(startTrig):
            startTrig.connect(partial(self.start), host=self)
        if isValid(finishTrig):
            finishTrig.connect(partial(self.quit), host=self)
        # noinspection PyUnresolvedReferences
        self._qtimer.timeout.connect(lambda: timer.updateValue(lambda a0: a0 + msecVal * self._delayMsec))

    def run(self):
        if self._running:
            return None
        self._running = True
        self._qtimer.start(self._delayMsec)
        self.exec_()
        return None

    def quit(self):
        self._running = False
        self._qtimer.stop()
        return super().quit()


class AsyncWorker(QObject):
    Workings = set()

    def __init__(
            self,
            thread: RActor,
            parent: QWidget = None,
            timer: RState[float] = None,
            delayMsec: int = None,
            onFinished: Callable = None,
    ):
        super().__init__()
        self._worker = thread
        self._parent = parent
        self._worker.setParent(self._parent)
        self._timer = RTimer(timer, delayMsec)
        self._timer.setParent(self._parent)
        # noinspection PyUnresolvedReferences
        self._worker.finished.connect(lambda: self.stop())
        # noinspection PyUnresolvedReferences
        self._worker.finished.connect(Validate(onFinished, lambda: None))

    def start(self):
        if self._parent in self.Workings:
            return None
        if isValid(self._parent):
            self.Workings.add(self._parent)
        self._worker.start()
        self._timer.start()
        return None

    def stop(self):
        self._timer.quit()
        if self._parent in self.Workings:
            self.Workings.remove(self._parent)
        return None
