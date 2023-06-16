import abc

class SemanticToken(metaclass=abc.ABCMeta):
    def is_semantic_token() -> bool:
        return True
    
    @abc.abstractmethod
    def __repr__(self) -> str:
        pass
    
    @abc.abstractmethod
    def __eq__(self, __value: "SemanticToken") -> bool:
        pass

class Padding(SemanticToken):
    def __init__(self) -> None:
        super().__init__()
    
    def __repr__(self) -> str:
        return "パディング"
    
    def __eq__(self, padding: SemanticToken) -> bool:
        return isinstance(padding, Padding)

class Note(SemanticToken):
    def __init__(self, pitch: int) -> None:
        super().__init__()
        self.pitch = pitch
    
    def __lt__(self, note: "Note") -> bool:
        return self.pitch < note.pitch
    
    def __eq__(self, note: SemanticToken) -> bool:
        return isinstance(note, Note) and self.pitch == note.pitch
    
    def __repr__(self) -> str:
        return f"音符（{self.pitch}）"

class Time(SemanticToken):
    def __init__(self, time: int) -> None:
        super().__init__()
        self.time = time
        
    def __eq__(self, time: SemanticToken) -> bool:
        return isinstance(time, Time) and self.time == time.time
    
    def __repr__(self) -> str:
        return f"時間（{self.time}）"

class NoteOnOff(SemanticToken):
    def __init__(self, on: bool) -> None:
        super().__init__()
        self.on = on

    def __repr__(self) -> str:
        return "鳴り始め" if self.on else "鳴り終わり"
    
    def __eq__(self, noteonoff: SemanticToken) -> bool:
        return isinstance(noteonoff, NoteOnOff) and self.on == noteonoff.on
    
class EndOfTie(SemanticToken):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return "タイ終了"
    
    def __eq__(self, endoftie: SemanticToken) -> bool:
        return isinstance(endoftie, EndOfTie)
    
class EndOfSeq(SemanticToken):
    def __init__(self) -> None:
        super().__init__()
    
    def __repr__(self) -> str:
        return "セグメント終了"
    
    def __eq__(self, endofseq: SemanticToken) -> bool:
        return isinstance(endofseq, EndOfSeq)
