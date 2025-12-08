from typing import Any, Callable, List

from DeclarativeQt.Resource.Grammars.RGrammar import ReferList, GList, JoinLists, SumNestedList, DataBox

GenMethod = Callable[[], Any]


class RGraphic:
    @staticmethod
    def uniformAllocate(source: int, dests: int, surround: bool = True, times: int = 0) -> List[int]:
        def distribute(
                px: GenMethod, py: GenMethod, tx: int, ty: int,
                sur: bool = False, depth: int = 0,
        ) -> List[Any]:
            if tx < ty:
                tx, ty = ty, tx
                px, py = py, px
            if ty <= 0:
                return ReferList(range(tx), lambda a0: px())
            if sur:
                gk = tx // int(ty + 1)
                fk = tx % int(ty + 1)
            else:
                gk = tx // ty
                fk = tx % ty
            place = lambda a0, a1, t0: ReferList(range(t0), lambda b0: a0()) + GList(a1())
            suffix = ReferList(range(gk), lambda a0: px()) if sur else GList()
            if depth > 0:
                array = DataBox(distribute(
                    px=lambda: place(px, py, gk),
                    py=lambda: place(px, py, gk + 1),
                    tx=ty - fk, ty=fk,
                    sur=sur, depth=depth - 1,
                )).data
            else:
                array = DataBox(JoinLists(
                    ReferList(range(ty - fk), lambda a0: place(px, py, gk)),
                    ReferList(range(fk), lambda a0: place(px, py, gk + 1)),
                )).data
            return list(SumNestedList(array) + suffix)

        times = max(times, 0)
        vak = source // dests
        rest = source % dests
        if times <= 0:
            left = ReferList(range(dests - rest), lambda a0: vak)
            right = ReferList(range(rest), lambda a0: vak + 1)
            return left + right
        return DataBox(distribute(
            px=lambda: vak, py=lambda: vak + 1,
            tx=dests - rest, ty=rest, sur=surround, depth=times - 1,
        )).data
