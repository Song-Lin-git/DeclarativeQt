import io
from io import BytesIO
from typing import List, Tuple

import PIL.Image
from PyQt5.QtCore import QSizeF
from PyQt5.QtGui import QPixmap, QImage
from matplotlib.figure import Figure
from reportlab.platypus import Image as RpbImage

from DeclarativeQt.Resource.FileTypes.RFileType import RFileType, FileType
from DeclarativeQt.Resource.Grammars.RGrammar import Validate
from DeclarativeQt.Resource.Images.RImage import LutExact, RImage
from DeclarativeQt.Resource.Strings.RStr import RStr

ImageType = str
PILImage = PIL.Image.Image


class PilGraphic:
    PNG: FileType = RFileType.png.upper()

    @staticmethod
    def fromMatplotFig(fig: Figure):
        buffer = BytesIO()
        fig.savefig(buffer, format=PilGraphic.PNG.lower())
        buffer.seek(0)
        image = PIL.Image.open(buffer)
        return image

    @staticmethod
    def toBytesArray(image: PILImage, form: ImageType = PNG) -> BytesIO:
        image_bytes = io.BytesIO()
        try:
            image.save(image_bytes, format=form)
        except Exception as e:
            RStr.log(str(e), RStr.lgError)
        image_bytes.seek(0)
        return image_bytes

    @staticmethod
    def toQPixmap(image: PILImage, form: ImageType = PNG) -> QPixmap:
        image_bytes = PilGraphic.toBytesArray(image, form)
        pixmap = QPixmap()
        pixmap.loadFromData(image_bytes.getvalue())
        return pixmap

    @staticmethod
    def toQImage(image: PILImage, form: ImageType = PNG):
        image_bytes = PilGraphic.toBytesArray(image, form)
        image = QImage()
        image.loadFromData(image_bytes.getvalue(), format=form)
        return image

    @staticmethod
    def toReportlabImages(
            images: List[PILImage], limitBox: QSizeF = None, pageSize: Tuple = None, scaleRatio: float = None
    ) -> List[RpbImage]:
        rpb_images = list()
        scaleRatio = Validate(scaleRatio, 1.0)
        for pil_image in images:
            image_stream = PilGraphic.toBytesArray(pil_image, RFileType.png.upper())
            if pageSize is None or len(pageSize) < 2 or limitBox is None:
                rpb_images.append(RpbImage(image_stream))
                continue
            page_width, page_height = pageSize[:2]
            limit_width, limit_height = page_width * limitBox.width(), page_height * limitBox.height()
            limit_box = QSizeF(limit_width, limit_height)
            target_size = RImage.limitImageToBox(QSizeF(pil_image.width, pil_image.height), limit_box)
            target_width = target_size.width() * scaleRatio
            target_height = target_size.height() * scaleRatio
            rpb_images.append(RpbImage(image_stream, width=target_width, height=target_height))
        return rpb_images

    @staticmethod
    def scaleToWidth(image: PILImage, width: LutExact) -> PILImage:
        ratio = width / image.width
        dimensions = width, int(ratio * image.height)
        return image.resize(dimensions)

    @staticmethod
    def scaleToHeight(image: PILImage, height: LutExact) -> PILImage:
        ratio = height / image.height
        dimensions = int(image.width * ratio), height
        return image.resize(dimensions)

    @staticmethod
    def scaleToSize(image: PILImage, width: LutExact, height: LutExact) -> PILImage:
        ratio = min(width / image.width, height / image.height)
        dimensions = int(image.width * ratio), int(image.height * ratio)
        return image.resize(dimensions)
