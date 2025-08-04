class FontArgs:
    def __init__(
            self,
            family: str = None,
            size: int = None,
            bold: bool = None,
            italic: bool = None,
            underline: bool = None
    ):
        self.family = family
        self.size = size
        self.bold = bold
        self.italic = italic
        self.underline = underline
