from typing import List, Dict
from collections import defaultdict

from mgenutils.token.SemanticToken import EndOfTie, SemanticToken, Time, Note, NoteOnOff, TimeLike

OnsetNotesMap = Dict[bool, List[Note]]

class Segment:
    tie: List[Note]
    time_event_map: defaultdict[int, OnsetNotesMap]
    
    def __init__(self, tokens: List[SemanticToken]) -> None:
        _endoftie = [
            idx for idx in range(len(tokens))
            if tokens[idx] == EndOfTie()
        ][0]
        
        self.tie = tokens[:_endoftie]
        
        self.time_event_map = defaultdict(lambda: { True: [], False: [] })
        
        cur_time  = None
        cur_onset = None
        for token in tokens[_endoftie + 1:len(tokens) - 1]:
            if isinstance(token, Time):
                cur_time = token.time
            elif isinstance(token, NoteOnOff):
                cur_onset = token.on
            elif isinstance(token, Note):
                self.time_event_map[cur_time][cur_onset].append(token)
            else:
                raise AssertionError(f"Unexpected type of token: {token}")
            
    
    def contains_as_tie(self, note: Note) -> bool:
        return note in self.tie
    
    def get_times(self) -> List[Time]:
        return [ Time(time) for time in self.time_event_map.keys() ]
    
    def __getitem__(self, time: TimeLike) -> OnsetNotesMap:
        return self.time_event_map[Time.to_int_time(time)]
    
    def __eq__(self, segment: "Segment") -> bool:
        def _are_shuffled_lists(x: list, y: list) -> bool:
            if len(x) == len(y):
                _x = sorted(x)
                _y = sorted(y)
                for i in range(len(x)):
                    if _x[i] != _y[i]:
                        return False
                return True
            else:
                return False
                
        # タイ部分が一致するか確認
        if not _are_shuffled_lists(self.tie, segment.tie):
            return False
        
        # event部分が一致するか確認
        time1 = self.get_times()
        time2 = segment.get_times()
        
        if _are_shuffled_lists(time1, time2):
            for time in time1:
                for b in [True, False]:
                    if not _are_shuffled_lists(self[time][b], segment[time][b]):
                        return False
            return True
        else:
            return False
    
        