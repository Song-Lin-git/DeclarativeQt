import os
from abc import ABC

from DeclarativeQt.Resource.Grammars.RGrammar import StrFrame, Equal
from DeclarativeQt.Resource.Strings.RString import RString

FileType = str
FileFilter = str
FilePath = str
FileName = str
FileOpenMode = str
FileDescription = str
FilterFrame: StrFrame = lambda description, suffix: str(description + f" (*.{suffix})")


class RSpecialFiles(ABC):
    ast: FileType = "ast"
    udi: FileType = "udi"
    dptAst: FileDescription = "App Settings"
    dptUdi: FileDescription = "User Data"
    fltAst: FileFilter = FilterFrame(dptAst, ast)
    fltUdi: FileFilter = FilterFrame(dptUdi, udi)


class RFileType:
    Spec = RSpecialFiles
    FileNameDivider = RString.pDot
    FilterDivider = ";;"
    ReadMode: FileOpenMode = "r"
    WriteMode: FileOpenMode = "w"
    ReadBinaryMode: FileOpenMode = "rb"

    @staticmethod
    def joinFilters(*filters: str):
        return RFileType.FilterDivider.join(filters)

    @staticmethod
    def makeFileName(extend: str, body: str = RString.pPlaceholder):
        return body + RFileType.FileNameDivider + extend

    @staticmethod
    def isFileType(fileName: str, fileType: str) -> bool:
        try:
            ext = os.path.splitext(fileName)[1][1:]
        except Exception as e:
            RString.log(str(e), RString.lgError)
            return False
        return Equal(ext, fileType)

    excel: FileType = "xlsx"
    pdf: FileType = "pdf"
    docx: FileType = "docx"
    png: FileType = "png"
    bmp: FileType = "bmp"
    jpg: FileType = "jpg"
    jpeg: FileType = "jpeg"
    html: FileType = "html"
    ttfont: FileType = "ttf"
    ttcollection: FileType = "ttc"
    fltExcel: FileFilter = "Excel Files (*.xlsx)"
    fltAll: FileFilter = "All Files (*)"
    fltPdf: FileFilter = "PDF Files (*.pdf)"
    fltDocx: FileFilter = "Word Files (*.docx)"
    fltPng: FileFilter = "PNG Files (*.png)"
    fltJpg: FileFilter = "JPG Files (*jpg)"
    fltBmp: FileFilter = "BMP Files (*bmp)"
    fltHtml: FileFilter = "HTML Files (*.html)"
