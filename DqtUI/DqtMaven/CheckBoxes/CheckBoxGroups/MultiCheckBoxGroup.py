import math
from functools import partial
from typing import Callable, List, Iterable, Dict

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

from DeclarativeQt.DqtCore.DqtBase import Remember, Run, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import BoolSTox, StringSTox, SeqToState, \
    ValToState, SmticToState
from DeclarativeQt.DqtUI.DqtLayouts.BaseLayouts.LinearLayout import LinearLayout
from DeclarativeQt.DqtUI.DqtMaven.CheckBoxes.IconCheckBox import IconCheckBox, CheckBoxStyle
from DeclarativeQt.DqtUI.DqtMaven.Dividers.LinearDivider import VerticalDivider, HorizontalDivider
from DeclarativeQt.DqtUI.DqtMaven.Spacers.LinearSpacer import HorizontalSpacer, VerticalSpacer
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import FixListLength, Validate, ReferList, inRange, JoinLists, GList, \
    Equal
from DeclarativeQt.Resource.Strings.RStr import RStr, NLIndex


class MultiCheckBoxGroup(LinearLayout):
    MainSpacerLengthRatio = 0.2
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
            onSelect: Callable[[List], None] = None,
            selection: Remember[List[int]] = None,
            language: RState[NLIndex] = None,
            selectAll: bool = False,
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
        checkBoxItems = SeqToState(checkBoxItems).value()
        total = len(checkBoxItems)
        checkBoxStates = SeqToState(
            FixListLength(Validate(checkBoxStates, list()), total, False)
        ).value()
        onChecked = FixListLength(Validate(onChecked, list()), total, lambda: None)
        checkBoxSize = Validate(checkBoxSize, self.DefaultCheckBoxSize)
        if fixedCheckBoxHeight:
            checkBoxSize.setHeight(fixedCheckBoxHeight)
        checkBoxSizes = ReferList(range(total), lambda a0: QSize(checkBoxSize))
        language = Validate(language, RStr.EN)
        if selectAll:
            checkBoxSizes.append(QSize(checkBoxSize))
            checkBoxItems.append(SmticToState(language, RStr.R.stSelectAll))
        selectAllState = Remember(False)
        maxWidth = checkBoxSize.width()
        if adaptiveCheckBoxWidth:
            for i, box in enumerate(checkBoxSizes):
                width = DqtCanvas.fontTextMetric(QFont(
                    Remember.getValue(styleEditor.getStyle(DqtStyle.atFontFamily)),
                    math.ceil(Remember.getValue(styleEditor.getStyle(DqtStyle.atFontSize)))
                ), Remember.getValue(checkBoxItems[i])).width()
                width += int(1.5 * checkBoxSize.height())
                maxWidth = max(maxWidth, width)
                box.setWidth(width)
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
            content=JoinLists(
                GList(
                    IconCheckBox(
                        size=checkBoxSizes[-1],
                        fixedHeight=fixedCheckBoxHeight,
                        fixedWidth=checkBoxSizes[-1].width() if fixCheckBoxWidth else None,
                        description=checkBoxItems[-1],
                        checked=selectAllState,
                        styleEditor=styleEditor,
                        onClick=lambda: Run(
                            ReferList(range(total), lambda idx: Run(
                                checkBoxStates[idx].setValue(selectAllState)
                            )), self.updateSelection(),
                        ),
                    ),
                    VerticalDivider(
                        length=checkBoxSize.height(), fixedLength=fixedCheckBoxHeight
                    ) if Equal(direction, LinearLayout.Horizontal) else
                    HorizontalDivider(length=checkBoxSize.width()),
                    HorizontalSpacer(width=int(
                        maxWidth * self.MainSpacerLengthRatio
                    ), fixed=True) if Equal(direction, LinearLayout.Horizontal) else
                    VerticalSpacer(height=int(
                        checkBoxSize.height() * self.MainSpacerLengthRatio
                    ), fixed=True)
                ) if selectAll else list(),
                ReferList(
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
                )
            ),
        )
        self._itemsCount = total
        self._checkBoxStates: BoolSTox = checkBoxStates
        self._selectAllState = selectAllState
        self._selection = ValToState(Validate(selection, list()))
        self._selection.connect(partial(Validate(onSelect, lambda lt: None)), host=self)
        trigger = Validate(trigger, dict())
        for k, v in trigger.items():
            k.connect(partial(v), host=self)

    @private
    def isValidIndex(self, idx: int):
        return inRange(idx, 0, self._itemsCount)

    def isAllSelected(self):
        selected = sum(ReferList(Remember.getListValue(self._checkBoxStates), lambda checked: 1 if checked else 0))
        return selected >= self._itemsCount

    def updateSelection(self):
        selected = list()
        for i, checked in enumerate(Remember.getListValue(self._checkBoxStates)):
            if checked:
                selected.append(i)
        self._selection.setValue(selected)
        return None

    def fixSelections(self, idx: int):
        if not self.isValidIndex(idx):
            return None
        if self._checkBoxStates[idx].equal(False):
            self._selectAllState.setValue(False)
        else:
            if self.isAllSelected():
                self._selectAllState.setValue(True)
        self.updateSelection()
        return None
