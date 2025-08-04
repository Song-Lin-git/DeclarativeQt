from functools import partial
from typing import Callable, List, Iterable, Dict

from PyQt5.QtCore import QSize

from DeclarativeQt.DqtCore.DqtBase import Remember, Run, RState
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import BoolSTox, StringSTox, SeqToRemember, \
    ValToRemember, SemanticRemember
from DeclarativeQt.DqtUI.DqtLayouts.BaseLayouts.LinearLayout import LinearLayout
from DeclarativeQt.DqtUI.DqtMaven.CheckBoxes.IconCheckBox import IconCheckBox, CheckBoxStyle
from DeclarativeQt.DqtUI.DqtMaven.Dividers.LinearDivider import VerticalDivider, HorizontalDivider
from DeclarativeQt.DqtUI.DqtMaven.Spacers.LinearSpacer import HorizontalSpacer, VerticalSpacer
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import FixListLength, Validate, LambdaList, inRange, JoinLists, GList, \
    Equal, DataBox
from DeclarativeQt.Resource.Strings.RString import RString, NLIndex


class MultiCheckBoxGroup(LinearLayout):
    DefaultCheckBoxSize = QSize(180, 30)
    MainSpacerLengthRatio = 0.2

    def __init__(
            self,
            size: QSize = None,
            checkBoxItems: StringSTox = None,
            checkBoxSize: QSize = None,
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
        checkBoxItems = SeqToRemember(checkBoxItems).value()
        count = len(checkBoxItems)
        checkBoxStates = SeqToRemember(FixListLength(Validate(checkBoxStates, list()), count, False)).value()
        onChecked = FixListLength(Validate(onChecked, list()), count, lambda: None)
        selectAllState = Remember(False)
        checkBoxSize = Validate(checkBoxSize, self.DefaultCheckBoxSize)
        language = Validate(language, RString.EnglishIndex)
        if fixedCheckBoxHeight:
            checkBoxSize.setHeight(fixedCheckBoxHeight)
        spaceBox: QSize = DataBox(QSize(
            int(checkBoxSize.width() * self.MainSpacerLengthRatio),
            int(checkBoxSize.height() * self.MainSpacerLengthRatio)
        )).data
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
                        size=checkBoxSize,
                        fixedHeight=fixedCheckBoxHeight,
                        description=SemanticRemember(language, RString.stSelectAll),
                        checked=selectAllState,
                        onClick=lambda: Run(
                            LambdaList(range(count), lambda i: Run(
                                checkBoxStates[i].setValue(selectAllState)
                            )),
                            self.updateSelection()
                        ),
                        styleEditor=styleEditor
                    ),
                    VerticalDivider(length=checkBoxSize.height(), fixedLength=fixedCheckBoxHeight)
                    if Equal(direction, LinearLayout.Horizontal) else
                    HorizontalDivider(length=checkBoxSize.width()),
                    HorizontalSpacer(width=spaceBox.width(), fixed=True)
                    if Equal(direction, LinearLayout.Horizontal) else
                    VerticalSpacer(height=spaceBox.height(), fixed=True)
                ) if selectAll else list(),
                LambdaList(
                    range(count), lambda i:
                    IconCheckBox(
                        size=checkBoxSize,
                        fixedHeight=fixedCheckBoxHeight,
                        description=checkBoxItems[i],
                        checked=checkBoxStates[i],
                        onClick=partial(self.fixSelections, i),
                        onValueChange=partial(onChecked[i]),
                        styleEditor=styleEditor,
                    )
                )
            ),
        )
        self._itemsCount = count
        self._checkBoxStates: BoolSTox = checkBoxStates
        self._selectAllState = selectAllState
        self._selection = ValToRemember(Validate(selection, list()))
        self._selection.connect(partial(Validate(onSelect, lambda lt: None)), host=self)
        trigger = Validate(trigger, dict())
        for k, v in trigger.items():
            k.connect(partial(v), host=self)

    @private
    def isValidIndex(self, idx: int):
        return inRange(idx, 0, self._itemsCount)

    def isAllSelected(self):
        selected = sum(LambdaList(Remember.getListValue(self._checkBoxStates), lambda checked: 1 if checked else 0))
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
