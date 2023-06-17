class MIDINote:
    start: int
    end  : int
    pitch: int
    scale: str
    def __init__(self, note=None) -> None:
        if note is None:
            pass
        else:
            self.start = note.start
            self.end   = note.end
            self.pitch = note.pitch
            self.scale = "original"

    def __repr__(self) -> str:
        return f"NOTE({self.pitch}): {self.start} ~ {self.end} in {self.scale} scale"
            
    def set_scale(self, scale, nframes_per_sec: int) -> None:
        if scale == "frame":
            if self.scale == "original":
                self.scale = "frame"
                self.start = round(nframes_per_sec * self.start)
                self.end   = round(nframes_per_sec * self.end)
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
    