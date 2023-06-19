from typing import List, Tuple
from mgenutils.midi import MIDIInstrument, MIDIFile, MIDINote

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

    def decode_segments_to_midi(segments: List[Segment], sec_per_segment: int) -> MIDIFile.MIDIFile:
        cur_time = 0
        on_notes: List[Tuple[Note, Time]] = []
        
        def get_time_of(notes: List[Tuple[Note, Time]], note: Note) -> Time:
            return [ n for n in notes if note == n[0] ][0][1]
        
        piano = MIDIInstrument.MIDIInstrument(program=0, notes=[])
        
        for segment in segments:
            piano.append([
                MIDINote.MIDINote(
                    velocity = 100,
                    pitch    = note[0].pitch,
                    start    = note[1],
                    end      = cur_time
                )
                for note in on_notes
                if not segment.contains_as_tie(note[0])
            ])
            
            on_notes = [
                note for note in on_notes
                if segment.contains_as_tie(note[0])
            ]
            
            for time in segment.get_times():
                events = segment[time]
                
                
                on_notes += [ (note, time + cur_time) for note in events[True] ]
                for note in events[False]:
                    piano.append(MIDINote.MIDINote(
                        velocity = 100,
                        pitch    = note.pitch,
                        start    = get_time_of(on_notes, note),
                        end      = time + cur_time
                    ))
                    on_notes = [ n for n in on_notes if n[0] != note ]
            
            # TODO
            cur_time += sec_per_segment

        return MIDIFile.MIDIFile([ piano ])
    