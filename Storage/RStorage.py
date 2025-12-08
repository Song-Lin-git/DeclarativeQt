import os

from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import CommandFrame

DirPath = str


class RStorage:
    AttribCommand: CommandFrame = lambda path: f"attrib +h {path}"

    def __init__(self):
        self._markRootHiden = False
        self._rootPath: DirPath = str(os.path.join(os.getcwd(), self.rootAppData))

    @private
    def hideRootDir(self):
        if self._markRootHiden:
            return None
        import win32api
        import win32con
        # noinspection PyUnresolvedReferences
        win32api.SetFileAttributes(self._rootPath, win32con.FILE_ATTRIBUTE_HIDDEN)
        self._markRootHiden = True

    def makeRoot(self):
        if not os.path.exists(self._rootPath):
            os.makedirs(self._rootPath, exist_ok=True)
        self.hideRootDir()
        return self._rootPath

    def getDir(self, dirPath: DirPath):
        dir_path = os.path.join(self._rootPath, dirPath)
        os.makedirs(dir_path, exist_ok=True)
        self.hideRootDir()
        return DirPath(dir_path)

    @property
    def rootPath(self):
        return self._rootPath

    rootAppData: DirPath = ".AppData"
    dirAppSetting: DirPath = ".AppSetting"
    dirUserData: DirPath = ".UserData"
    dirFontCache: DirPath = ".TTFontCache"
    dirIconCache: DirPath = ".IconCache"
