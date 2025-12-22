import os
from pathlib import Path

from RBase.Grammars.RGram import GTuple, Equal

_ThisFilePath = __file__


class RGenIcons:
    Root = Path(_ThisFilePath).resolve().parent
    Tar = Path("IconSource/Icons")
    Source = Root / f"{Tar}"
    Dest = Root / f"{Tar}.py"
    SybTab = " " * 4
    Allows = GTuple("PNG", "JPG", "JPEG", "BMP")

    @classmethod
    def build(cls, deep: bool = False):
        icons = list()
        for root, dirs, files in os.walk(cls.Source):
            rel_root = os.path.relpath(root, f"{cls.Source}")
            for file in files:
                for tp in cls.Allows:
                    if file.lower().endswith(tp.lower()):
                        if Equal(f"{rel_root}", "."):
                            icons.append(file)
                        elif deep:
                            icons.append(f"{rel_root}/{file}")
        lines = list()
        with open(f"{cls.Dest}", 'r') as script:
            while line := script.readline():
                lines.append(line)
                if "class" in line:
                    break
        indent = cls.SybTab
        with open(f"{cls.Dest}", 'w') as script:
            script.writelines(lines)
            if not icons:
                script.write(f"{indent}pass\n")
            else:
                for icon in icons:
                    name = os.path.splitext(icon)[0].replace("/", "_")
                    name = name.replace(".", "_")
                    script.write(f"{indent}{name} = '{icon}'\n")
        return cls
