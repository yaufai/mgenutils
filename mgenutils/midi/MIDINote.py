from typing import Literal, Union
import pretty_midi as pm
from mgenutils.token.SemanticToken import TimeLike, Time

MIDINoteScale = Literal["original", "frame"]

class MIDINote:
    velocity: int
    start   : int
    end     : int
    pitch   : int
    scale   : MIDINoteScale
    nframes_per_sec: Union[None, int]
    def __init__(self, velocity, start: TimeLike, end: TimeLike, pitch, scale="original") -> None:
        self.velocity = velocity
        self.start    = Time.to_int_time(start)
        self.end      = Time.to_int_time(end)
        self.pitch    = pitch
        self.scale    = scale
        self.nframes_per_sec = None
    
    def __eq__(self, note: "MIDINote") -> bool:
        return all([
            self.velocity == note.velocity,
            self.pitch    == note.pitch,
            self.start    == note.start,
            self.end      == note.end,
            self.scale    == note.scale,
            self.nframes_per_sec == note.nframes_per_sec,
        ])

    def __repr__(self) -> str:
        return f"NOTE({self.pitch}): {self.start} ~ {self.end} in {self.scale} scale at velocity {self.velocity}"
            
    def set_scale(self, scale, nframes_per_sec: int) -> None:
        if scale == "frame":
            if self.scale == "original":
                self.scale = "frame"
                self.start = round(nframes_per_sec * self.start)
                self.end   = round(nframes_per_sec * self.end)
                self.nframes_per_sec = nframes_per_sec
        else:
            raise NotImplementedError()
        
    def begins_between(self, start: int, end: int) -> bool:
        start_condition = self.start >= start
        end_condition   = self.start <= end
        return (start_condition) and (end_condition)
    
    def ends_between(self, start: int, end:int) -> bool:
        start_condition = self.end >= start
        end_condition   = self.end <= end
        return (start_condition) and (end_condition)
    
    def ends_before(self, start: int, true_if_simultaneous=False) -> bool:
        return self.end <= start if true_if_simultaneous else self.end < start
    
    def begins_after(self, end: int) -> bool:
        return self.start > end
    
    def begins_before(self, start: int, true_if_simultaneous=False) -> bool:
        return self.start <= start if true_if_simultaneous else self.start < start
    
    def ends_after(self, end: int) -> bool:
        return self.end > end

def convert_pm_note(note) -> MIDINote:
    return MIDINote(
        velocity = note.velocity,
        start    = note.start,
        end      = note.end,
        pitch    = note.pitch
    )

def convert_to_pm_note(note: MIDINote):
    scale = (1 / note.nframes_per_sec) if note.scale == "frame" else 1
    return pm.Note(
        note.velocity,
        note.pitch,
        note.start * scale,
        note.end   * scale
    )
