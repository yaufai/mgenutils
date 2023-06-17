from typing import List
from mgenutils.midi.MIDINote import MIDINote

class MIDIInstrument:
    notes  : List[MIDINote]
    program: int
    def __init__(self, instrument):
        self.notes = [
            MIDINote(note)
            for note in instrument.notes
        ]
        self.program = instrument.program