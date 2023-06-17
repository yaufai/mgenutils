import dataclasses

@dataclasses.dataclass
class MIDIEvent:
    program  : int
    onset    : bool
    pitch    : int

    def __le__(self, e) -> bool:
        if self.program == e.program:
            return not self.onset
        else:
            return self.program < e.program

    def __lt__(self, e) -> bool:
        return self <= e

    def __ge__(self, e) -> bool:
        if self.program == e.program:
            return self.onset
        else:
            return self.program > e.program