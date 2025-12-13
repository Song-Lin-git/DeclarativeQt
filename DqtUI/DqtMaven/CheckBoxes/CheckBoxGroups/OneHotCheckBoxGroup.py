import math
from functools import partial
from typing import Iterable, Dict, Callable, List

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import StringSTox, BoolSTox, SeqToRemember, \
    ValToRemember
from DeclarativeQt.DqtUI.DqtLayouts.BaseLayouts.LinearLayout import LinearLayout
from DeclarativeQt.DqtUI.DqtMaven.CheckBoxes.IconCheckBox import IconCheckBox, CheckBoxStyle
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, FixListLength, ReferList, inRange, isValid


class OneHotCheckBoxGroup(LinearLayout):
    DefaultCheckBoxSize = QSize(180, 30)

    def __init__(
            self,
            size: QSize = None,
            checkBoxItems: StringSTox = None,
            checkBoxSize: QSize = None,
            adaptiveCheckBoxWidth: bool = False,
            fixCheckBoxWidth: bool = False,
            fixedCheckBoxHeight: int = None,
            checkBoxStates: BoolSTox = None,
            onChecked: List[Callable] = None,
            onSelect: Callable[[int], None] = None,
            selection: Remember[int] = None,
            forcedCheck: bool = False,
            direction: str = LinearLayout.Vertical,
            options: Iterable = None,
            alignment: int = None,
            arrangement: int = None,
            spacing: int = None,
            linePadding: int = None,
            crossPadding: int = None,
            style: RState[str] = None,
            trigger: Dict[Remember, Callable] = None,
            styleEditor: CheckBoxStyle = None
    ):
        checkBoxItems = SeqToRemember(checkBoxItems).value()
        total = len(checkBoxItems)
        checkBoxStates = SeqToRemember(
            FixListLength(Validate(checkBoxStates, list()), total, False)
        ).value()
        checkBoxSize = Validate(checkBoxSize, self.DefaultCheckBoxSize)
        if fixedCheckBoxHeight:
            checkBoxSize.setHeight(fixedCheckBoxHeight)
        checkBoxSizes = ReferList(range(total), lambda a0: QSize(checkBoxSize))
        if adaptiveCheckBoxWidth:
            for i, box in enumerate(checkBoxSizes):
                width = DqtCanvas.fontTextMetric(QFont(
                    Remember.getValue(styleEditor.getStyle(DqtStyle.atFontFamily)),
                    math.ceil(Remember.getValue(styleEditor.getStyle(DqtStyle.atFontSize)))
                ), Remember.getValue(checkBoxItems[i])).width()
                width += int(1.5 * checkBoxSize.height())
                box.setWidth(width)
        onChecked = FixListLength(Validate(onChecked, list()), total, lambda: None)
        super().__init__(
            size=size,
            direction=direction,
            options=options,
            alignment=alignment,
            arrangement=arrangement,
            spacing=spacing,
            linePadding=linePadding,
            crossPadding=crossPadding,
            style=style,
            content=ReferList(
                range(total), lambda idx:
                IconCheckBox(
                    size=checkBoxSizes[idx],
                    fixedHeight=fixedCheckBoxHeight,
                    fixedWidth=checkBoxSizes[idx].width() if fixCheckBoxWidth else None,
                    description=checkBoxItems[idx],
                    checked=checkBoxStates[idx],
                    onClick=partial(self.fixSelections, idx),
                    onValueChange=partial(onChecked[idx]),
                    styleEditor=styleEditor,
                )
            ),
        )
        self._forcedCheck = forcedCheck
        self._itemsCount = total
        self._checkBoxStates: BoolSTox = checkBoxStates
        self._selection = ValToRemember(selection)
        if forcedCheck:
            self._selection.updateValue(lambda a0: 0 if a0 is None else a0)
        if isValid(self._selection.value()):
            self._selection.updateValue(lambda a0: min(total - 1, max(0, a0)))
            self.fixSelections(self._selection.value())
        self._selection.connect(partial(Validate(onSelect, lambda idx: None)), host=self)
        trigger = Validate(trigger, dict())
        for k, v in trigger.items():
            k.connect(partial(v), host=self)

    @private
    def isValidIndex(self, idx: int):
        return inRange(idx, 0, self._itemsCount)

    def fixSelections(self, idx: int):
        if not self.isValidIndex(idx):
            return None
        if self._checkBoxStates[idx].equal(True):
            self._selection.setValue(idx)
            for i, state in enumerate(self._checkBoxStates):
                if i != idx:
                    state.setValue(False)
        else:
            if self._forcedCheck:
                self._checkBoxStates[idx].setValue(True)
            else:
                self._selection.setValue(None)
        return None
