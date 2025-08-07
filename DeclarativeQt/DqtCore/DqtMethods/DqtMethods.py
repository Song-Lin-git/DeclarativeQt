from functools import partial
from typing import List, Optional, Union

from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit

from DeclarativeQt.DqtCore.DqtBase import Remember
from DeclarativeQt.DqtUI.DqtLayouts.BaseLayouts.BoxLayout import BoxLayout
from DeclarativeQt.DqtUI.DqtLayouts.BaseLayouts.LinearLayout import LinearLayout
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BaseButton.Button import Button
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BaseTextField.TextField import TextField
from DeclarativeQt.Resource.Grammars.RGrammar import ReferList, isValid, CheckType, NxLimitVal, ConditionList, GList, \
    Equal


class DqtMethods:
    Layout = Union[BoxLayout, LinearLayout]

    @staticmethod
    def findTypedChildContents(
            layout: QWidget, *tp: type,
            depth: int = +1, strict: bool = False
    ) -> Optional[List[QWidget]]:
        tp = ConditionList(list(tp), lambda a0: issubclass(a0, QWidget))
        if len(tp) <= 0 or depth < 0:
            return None
        if Equal(depth, 0):
            return GList(layout) if CheckType(layout, Union[tuple(tp)]) else None
        if not CheckType(layout, DqtMethods.Layout):
            return None
        qak = DqtMethods.getLayoutContents(layout)
        results = list()
        for i in range(depth):
            qx, reached = list(), int(i + 1) >= depth
            for item in qak:
                if not strict or reached:
                    if CheckType(item, Union[tuple(tp)]):
                        results.append(item)
                if not reached and CheckType(item, DqtMethods.Layout):
                    qx += DqtMethods.getLayoutContents(item)
            qak = qx.copy()
        return results

    @staticmethod
    def getLayoutContents(layout: Layout) -> Optional[List[QWidget]]:
        if not CheckType(layout, DqtMethods.Layout):
            return None
        isBox = CheckType(layout, BoxLayout)
        if not isBox:
            return list(layout.contents)
        return GList(Remember.getValue(layout.content))

    @staticmethod
    def backtrackParent(widget: QWidget, level: int = -1, flex: bool = False) -> Optional[QWidget]:
        pt, uiChain = widget, list()
        while isValid(pt):
            uiChain.append(pt)
            pt = pt.parent()
        if len(uiChain) <= 0:
            return None
        try:
            result = uiChain[level]
        except IndexError:
            if not flex:
                return None
            result = uiChain[0] if level < 0 else uiChain[-1]
        return result

    @staticmethod
    def backtrackTypedParent(
            widget: QWidget, *tp: type,
            reverse: bool = False, skip: int = 0,
    ) -> Optional[QWidget]:
        it, found = widget, list()
        if len(tp) > 0:
            tp = ConditionList(list(tp), lambda a0: issubclass(a0, QWidget))
        else:
            tp = GList(QWidget)
        if len(tp) <= 0:
            return None
        while isValid(it):
            if CheckType(it, Union[tuple(tp)]):
                found.append(it)
            it = it.parent()
        if len(found) <= 0:
            return None
        skip = NxLimitVal(skip, 0, len(found) - 1)
        found = found if not reverse else found[::-1]
        return found[skip]

    @staticmethod
    def findChildButtons(widget: QWidget) -> List[Button]:
        result = list()
        for child in widget.findChildren(QPushButton):
            if isinstance(child, Button):
                result.append(child)
        return result

    @staticmethod
    def findChildTextFields(widget: QWidget) -> List[TextField]:
        result = list()
        for child in widget.findChildren(QLineEdit):
            if isinstance(child, TextField):
                result.append(child)
        return result

    @staticmethod
    def buildSafeShortCutsForWidget(widget: QWidget) -> None:
        buttons = DqtMethods.findChildButtons(widget)
        textFields = DqtMethods.findChildTextFields(widget)
        enableShortCuts = lambda a0, a1: a0.disableShortCuts() if bool(a1) else a0.restoreShortCuts()
        completerMethod = lambda a0: ReferList(buttons, lambda b0: enableShortCuts(b0, a0))
        for editor in textFields:
            editor.setCompleterMethod(partial(completerMethod))
        return None
