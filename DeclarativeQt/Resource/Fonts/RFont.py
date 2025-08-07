import os
from typing import Union, Dict

import fontTools.ttLib
import matplotlib.font_manager as fm
from PyQt5.QtGui import QFont
from fontTools.ttLib import TTFont, TTCollection

from DeclarativeQt.Resource.FileTypes.RFileType import RFileType, FileType, FilePath
from DeclarativeQt.Resource.Fonts.FontBase import FontBase
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import GIters, ConditionList, \
    SumNestedList, ReferList, isEmpty, DictData, Key, Validate
from DeclarativeQt.Resource.Grammars.RGrmBase.RGrmBase import DataBox
from DeclarativeQt.Resource.Strings.RString import Symbol, RString
from DeclarativeQt.Storage.RStorage import RStorage

FontName = str
FontStyle = str
FontSize = int
FontArgs = FontBase.FontArgs


class RFont:
    fzDefaultSize: FontSize = int(12)
    fzTinySize: FontSize = int(9)
    fzSmallSize: FontSize = int(10)
    fzDefaultSubtitleSize: FontSize = int(14)
    fzDefaultTitleSize: FontSize = int(18)

    def __init__(self):
        self.EastAsiaFont = GIters(self.SongTi, self.HeiTi, self.SimHei, self.SimSun, self.YaHei)
        self._ttf: FileType = RFileType.ttfont
        self._ttc: FileType = RFileType.ttcollection
        self._regular: FontStyle = "regular"
        self._ttfNameField: Symbol = "name"
        self._fontFileNames: Dict = DictData(
            Key(self.SongTi).Val(self.SimSun.lower()),
            Key(self.HeiTi).Val(self.SimHei.lower()),
            Key(self.TNR).Val(self.TNR.split()[0].lower()),
            Key(self.YaHei).Val(RString.pMsyh),
            Key(self.CambriaMath).Val(RString.pCambria)
        ).data

    def getQFont(self, family: str, size: int = None, args: FontArgs = None) -> QFont:
        font = QFont()
        font.setFamily(family)
        font.setPointSize(Validate(size, self.fzDefaultSize))
        if args is None:
            return font
        bold, italic, underline = args.bold, args.italic, args.underline
        font.setBold(Validate(bold, False))
        font.setItalic(Validate(italic, False))
        font.setUnderline(Validate(underline, False))
        return font

    def defaultQFont(self):
        return self.getQFont(self.SimSun, size=self.fzDefaultSize)

    def defaultTitleQFont(self):
        return self.getQFont(self.SimHei, size=self.fzDefaultTitleSize, args=FontArgs(bold=True))

    @private
    def getFontFileName(self, fontName: FontName):
        if fontName in self._fontFileNames:
            return self._fontFileNames[fontName]
        return fontName.lower()

    @private
    def getTTFontSubfamilyName(self, ttf: fontTools.ttLib.TTFont):
        name = ttf[self._ttfNameField]
        return str(name.getName(2, 3, 1).toStr())

    def loadTTFont(self, fontName: FontName) -> Union[str, None]:
        cache_dir = RStorage().getDir(RStorage.dirFontCache)
        file_name = RFileType().makeFileName(self._ttf, self.getFontFileName(fontName))
        cache_path = os.path.join(cache_dir, file_name)
        return str(cache_path) if os.path.exists(cache_path) else None

    def cacheTTFont(self, fontName: FontName) -> Union[FilePath, None]:
        font_file = self.getFontFileName(fontName)
        font_paths = DataBox(ReferList(GIters(self._ttf, self._ttc), lambda font_ext: ConditionList(
            fm.findSystemFonts(fontpaths=None, fontext=font_ext), lambda file: font_file in file.lower()
        ))).data
        font_paths = SumNestedList(font_paths)
        font_path, extend_name = None, None
        for item in font_paths:
            font_path = item
            base_name, extend_name = os.path.splitext(os.path.basename(font_path))
            if str(base_name).lower() in GIters(font_file):
                break
        if not extend_name or isEmpty(extend_name):
            return None
        extend_name = str(extend_name[1:]).lower()
        cache_dir = RStorage().getDir(RStorage.dirFontCache)
        file_name = RFileType().makeFileName(self._ttf, font_file)
        cache_path = os.path.join(cache_dir, file_name)
        if extend_name in GIters(self._ttf):
            ttf = TTFont(font_path)
            ttf.save(cache_path)
        elif extend_name in GIters(self._ttc):
            ttc = TTCollection(font_path)
            if isEmpty(ttc.fonts):
                return None
            cached = False
            for font in ttc.fonts:
                if self.getTTFontSubfamilyName(font).lower() in GIters(self._regular):
                    font.save(cache_path)
                    cached = True
                    break
            if not cached:
                ttc.fonts[-1].save(cache_path)
        else:
            return None
        return FilePath(cache_path)

    SongTi: FontName = "宋体"
    HeiTi: FontName = "黑体"
    SimHei: FontName = "SimHei"
    Courier: FontName = "Courier New"
    SimSun: FontName = "SimSun"
    Kai: FontName = "KaiTi"
    TNR: FontName = "Times New Roman"
    SegoeUI: FontName = "Segoe UI"
    YaHei: FontName = "Microsoft YaHei"
    YaHeiLight: FontName = "Microsoft YaHei Light"
    JhengHei: FontName = "Microsoft JhengHei"
    CambriaMath: FontName = "CambriaMath"
