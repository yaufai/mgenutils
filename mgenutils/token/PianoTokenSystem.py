from typing import List

from mgenutils.token.Segment       import Segment
from mgenutils.token.TokenSystem   import RawToken, TokenSystem
from mgenutils.token.SemanticToken import SemanticToken, Note, NoteOnOff, EndOfSeq, EndOfTie, Time, Padding

NUM_OF_PITCHES = 128
NUM_OF_ONSETS  = 2
PIANO_PROGRAM  = 0

class PianoTokenSystem(TokenSystem):
    def __init__(self) -> None:
        super().__init__()
    
    def encode_segment(segment: Segment) -> List[RawToken]:
        return super().encode_segment()
    
    def encode_token(token: SemanticToken) -> RawToken:
        if isinstance(token, Padding):
            return 0
        elif isinstance(token, EndOfSeq):
            return 1
        elif isinstance(token, EndOfTie):
            return 2
        elif isinstance(token, Note):
            return 3 + token.pitch
        elif isinstance(token, NoteOnOff):
            return 3 + NUM_OF_PITCHES + (1 if token.on else 0)
        elif isinstance(token, Time):
            return 3 + NUM_OF_PITCHES + NUM_OF_ONSETS + token.time
        else:
            raise NotImplementedError()
    
    def decode_token(token: RawToken) -> SemanticToken:
        if token == 0:
            return Padding()
        elif token == 1:
            return EndOfSeq()
        elif token == 2:
            return EndOfTie()
        elif token <= 2 + NUM_OF_PITCHES:
            return Note(token - 3)
        elif token <= 2 + NUM_OF_PITCHES + NUM_OF_ONSETS:
            value = token - 3 - NUM_OF_PITCHES
            return NoteOnOff(value == 1)
        else:
            return Time(token - 3 - NUM_OF_PITCHES - NUM_OF_ONSETS) 
