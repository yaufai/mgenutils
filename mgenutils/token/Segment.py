from typing import List
from mgenutils.token.SemanticToken import EndOfTie, SemanticToken, Time, Note, NoteOnOff, EndOfSeq

Segment = List[SemanticToken]

def are_equivalent(seg1: Segment, seg2: Segment) -> bool:
    if len(seg1) != len(seg2):
        return False
    
    # タイ部分が一致するか確認

    def _idx_end_of_tie(lst) -> int:
        for i in range(len(lst)):
            if isinstance(lst[i], EndOfTie):
                return i 
        return -1
    
    tie_idx1 = _idx_end_of_tie(seg1)
    tie_idx2 = _idx_end_of_tie(seg2)
    
    if tie_idx1 != tie_idx2:
        return False
    
    tie_seg1 = sorted(seg1[:tie_idx1])
    tie_seg2 = sorted(seg2[:tie_idx2])
    
    for i in range(tie_idx1):
        if tie_seg1[i] != tie_seg2[i]:
            return False
    
    # event部分が一致するか確認
    
    events_seg1 = seg1[tie_idx1 + 1: ]
    events_seg2 = seg2[tie_idx2 + 1: ]
    

    
    def _check_equivalence(ns1, ns2) -> bool:
        _ns1 = sorted(ns1)
        _ns2 = sorted(ns2)
        for i in range(len(ns1)):
            if _ns1[i] == _ns2[i]:
                continue
            else:
                return False
            
        
        return True
            
    notes_1 = []
    notes_2 = []
    for i in range(len(events_seg1)):
        if isinstance(events_seg1[i], Time) and isinstance(events_seg2[i], Time):
            if events_seg1[i] != events_seg2[i]:
                return False
            if _check_equivalence(notes_1, notes_2):
                notes_1 = []
                notes_2 = []
            else:
                return False
        elif isinstance(events_seg1[i], NoteOnOff) and isinstance(events_seg2[i], NoteOnOff):
            if events_seg1[i] != events_seg2[i]:
                return False
            if _check_equivalence(notes_1, notes_2):
                notes_1 = []
                notes_2 = []
            else:
                return False
        elif isinstance(events_seg1[i], Note) and isinstance(events_seg2[i], Note):
            notes_1.append(events_seg1[i])
            notes_2.append(events_seg2[i])
        elif isinstance(events_seg1[i], EndOfSeq) and isinstance(events_seg2[i], EndOfSeq):
            return _check_equivalence(notes_1, notes_2)
        else:
            return False
            
    return True