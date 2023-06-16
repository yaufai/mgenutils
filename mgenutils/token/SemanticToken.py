import abc

class SemanticToken(metaclass=abc.ABCMeta):
    def is_semantic_token() -> bool:
        return True
    
    @abc.abstractmethod
    def __repr__(self) -> str:
        pass

class Padding(SemanticToken):
    def __init__(self) -> None:
        super().__init__()
    
    def __repr__(self) -> str:
        return "パディング"

class Note(SemanticToken):
    def __init__(self, pitch: int) -> None:
        super().__init__()
        self.pitch = pitch
    
    def __lt__(self, note: "Note") -> bool:
        return self.pitch < note.pitch
    
    def __eq__(self, note: "Note") -> bool:
        return self.pitch == note.pitch
    
    def __repr__(self) -> str:
        return f"音符（{self.pitch}）"

class Time(SemanticToken):
    def __init__(self, time: int) -> None:
        super().__init__()
        self.time = time
        
    def __eq__(self, time: "Time") -> bool:
        return self.time == time.time
    
    def __repr__(self) -> str:
        return f"時間（{self.time}）"

class NoteOnOff(SemanticToken):
    def __init__(self, on: bool) -> None:
        super().__init__()
        self.on = on

    def __repr__(self) -> str:
        return "鳴り始め" if self.on else "鳴り終わり"
    
class EndOfTie(SemanticToken):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return "タイ終了"
    
class EndOfSeq(SemanticToken):
    def __init__(self) -> None:
        super().__init__()
    
    def __repr__(self) -> str:
        return "セグメント終了"
