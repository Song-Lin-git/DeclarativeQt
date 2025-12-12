import base64
import io
import os.path
from abc import ABC
from typing import Callable, List

from PyQt5.QtCore import QIODevice, QBuffer
from PyQt5.QtGui import QPixmap, QImage
from bs4 import BeautifulSoup

from DeclarativeQt.Resource.FileTypes.RFileType import FileOpenMode, RFileType, FileType, FilePath
from DeclarativeQt.Resource.Grammars.RGrammar import StrFrame, isEmpty
from DeclarativeQt.Resource.Graphics.GtrTools.GtrPillow import PILImage
from DeclarativeQt.Resource.Images.RImage import LutExact, RImage

HtmlCode = str
HtmlElement = str


class HtmlGraphic(ABC):
    DefaultWidth: LutExact = RImage.exDefaultWidth

    @staticmethod
    def convertImagesToBase64(html: str, imagePaths: List[FilePath], width: int = DefaultWidth):
        encoder = HtmlBase64Encoder()
        return encoder.encodeImagesToBase64(encoder.imageToBase64, html, imagePaths, width)

    @staticmethod
    def convertQImagesToBase64(html: str, qImages: List[QImage], width: int = DefaultWidth):
        encoder = HtmlBase64Encoder()
        return encoder.encodeImagesToBase64(encoder.qImageToBase64, html, qImages, width)

    @staticmethod
    def convertPilsToBase64(html: str, pilImages: List[PILImage], width: int = DefaultWidth):
        encoder = HtmlBase64Encoder()
        return encoder.encodeImagesToBase64(encoder.pilImageToBase64, html, pilImages, width)


class HtmlBase64Encoder:
    def __init__(self):
        self._htmlDevice: HtmlElement = "html.parser"
        self._imgTag: HtmlElement = "img"
        self._srcField: HtmlElement = "src"
        self._widthField: HtmlElement = "width"
        self._heightField: HtmlElement = "height"
        self._autoMode: HtmlElement = "auto"
        self._imageDataFrame: StrFrame = lambda imData: f"data:image/png;base64,{imData}"
        self._RbMode: FileOpenMode = RFileType.ReadBinaryMode
        self._PNG: FileType = RFileType.png.upper()

    def encodeImagesToBase64(self, method: Callable, html: str, images: list, width: int):
        beautiful_soup = BeautifulSoup(html, self._htmlDevice)
        for img_tag in beautiful_soup.find_all(self._imgTag):
            if isEmpty(images):
                break
            image, images = images[0], images[1:]
            base64_data = method(image)
            img_tag[self._srcField] = self._imageDataFrame(base64_data)
            img_tag[self._widthField] = f"{width}"
            img_tag[self._heightField] = self._autoMode
        beautiful_soup = HtmlCode(beautiful_soup)
        return beautiful_soup

    def imageToBase64(self, imagePath: FilePath):
        if not os.path.exists(imagePath):
            return HtmlCode()
        with open(imagePath, self._RbMode) as image_file:
            image_bytes = image_file.read()
            assert isinstance(image_bytes, bytes)
            base64_data = base64.b64encode(image_bytes)
        return base64_data.decode()

    def qImageToBase64(self, qImage: QImage):
        if qImage.isNull():
            return HtmlCode()
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        QPixmap.fromImage(qImage).save(buffer, self._PNG)
        base64_data = base64.b64encode(bytes(buffer.data()))
        return base64_data.decode()

    def pilImageToBase64(self, pilImage: PILImage):
        buffer = io.BytesIO()
        pilImage.save(buffer, format=self._PNG)
        base64_data = base64.b64encode(buffer.getvalue())
        return base64_data.decode()
