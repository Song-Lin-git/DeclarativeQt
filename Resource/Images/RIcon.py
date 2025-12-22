import os
import shutil
from pathlib import Path
from typing import Union

from PyQt5.QtGui import QPixmap

from DeclarativeQt.Resource.FileTypes.RFileType import FilePath
from DeclarativeQt.Resource.Images.IconSource.Icons import Icons
from DeclarativeQt.Storage.RStorage import RStorage

_ThisFilePath = __file__

IconName = str


class RIcon:
    R = Icons
    IconSourceAt = Path(r"IconSource/Icons")
    SourceDirAt = Path(_ThisFilePath).resolve().parent / IconSourceAt
    CacheDirAt = RStorage().getDir(RStorage.dirIconCache)

    @staticmethod
    def loadIconPixmap(iconName: str) -> Union[QPixmap, None]:
        cachePath = RIcon.getIconCachePath(iconName)
        if not os.path.exists(cachePath):
            if RIcon.cacheIconSource(iconName) is None:
                return None
        return QPixmap(cachePath)

    @staticmethod
    def loadIconPath(iconName: str) -> Union[str, None]:
        cachePath = RIcon.getIconCachePath(iconName)
        if not os.path.exists(cachePath):
            if RIcon.cacheIconSource(iconName, pix=False) is None:
                return None
        return str(cachePath)

    @staticmethod
    def cacheIconSource(sourceName: str, pix: bool = True) -> Union[str, None]:
        sourcePath = RIcon.getIconSourcePath(sourceName)
        if not os.path.exists(sourcePath):
            return None
        cachePath = RIcon.getIconCachePath(sourceName)
        shutil.copy(sourcePath, cachePath)
        return str(sourcePath) if not pix else QPixmap(sourcePath)

    @staticmethod
    def getIconCachePath(iconName: str) -> FilePath:
        path = os.path.join(RIcon.CacheDirAt, iconName)
        return str(path)

    @staticmethod
    def getIconSourcePath(iconName: str) -> FilePath:
        path = os.path.join(RIcon.SourceDirAt, iconName)
        return str(path)
