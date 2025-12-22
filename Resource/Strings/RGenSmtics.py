from pathlib import Path

import yaml

_ThisFilePath = __file__


class RGenSmtics:
    Root = Path(_ThisFilePath).resolve().parent
    Tar = "NLSource/Strings"
    Source = Root / f"{Tar}.yaml"
    Dest = Root / f"{Tar}.py"
    SybTab = " " * 4
    VarSmtic = "semantic"

    @classmethod
    def build(cls):
        with open(f"{cls.Source}", 'r', encoding='utf-8') as file:
            loader = dict(yaml.safe_load(file))
        lines = list()
        with open(f"{cls.Dest}", 'r') as script:
            while line := script.readline():
                lines.append(line)
                if f"{cls.VarSmtic} = " in line:
                    break
        indent = cls.SybTab
        with open(f"{cls.Dest}", 'w') as script:
            script.writelines(lines)
            for k in loader.keys():
                script.write(f"{indent}{k} = {cls.VarSmtic}['{k}']\n")
        return cls
