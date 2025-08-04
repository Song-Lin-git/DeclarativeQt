from functools import partial
from typing import Iterable, Dict, Callable, List

from PyQt5.QtCore import QSize

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import StringSTox, BoolSTox, SeqToRemember, \
    ValToRemember
from DeclarativeQt.DqtUI.DqtLayouts.BaseLayouts.LinearLayout import LinearLayout
from DeclarativeQt.DqtUI.DqtMaven.CheckBoxes.IconCheckBox import IconCheckBox, CheckBoxStyle
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, FixListLength, LambdaList, inRange


class OneHotCheckBoxGroup(LinearLayout):
    def __init__(
            self,
            size: QSize = None,
            checkBoxItems: StringSTox = None,
            checkBoxSize: QSize = None,
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
        count = len(checkBoxItems)
        checkBoxStates = SeqToRemember(FixListLength(Validate(checkBoxStates, list()), count, False)).value()
        onChecked = FixListLength(Validate(onChecked, list()), count, lambda: None)
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
            content=LambdaList(
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
            ),
        )
        self._forcedCheck = forcedCheck
        self._itemsCount = count
        self._checkBoxStates: BoolSTox = checkBoxStates
        self._selection = ValToRemember(selection)
        self._selection.connect(partial(Validate(onSelect, lambda i: None)), host=self)
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
