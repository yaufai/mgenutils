from typing import List, Union
import pretty_midi as pm
from mgenutils.midi.MIDINote import MIDINote, convert_pm_note, convert_to_pm_note

class MIDIInstrument:
    notes  : List[MIDINote]
    program: int
    
    def __init__(self, notes: List[MIDINote], program: int):
        self.notes   = notes
        self.program = program
    
    def append(self, note: Union[MIDINote, List[MIDINote]]):
        if isinstance(note, MIDINote):
            self.notes.append(note)
        else:
            self.notes += note
        
def convert_pm_instrument(instrument) -> MIDIInstrument:
    return MIDIInstrument(
        [
            convert_pm_note(note) for note in instrument.notes
        ],
        instrument.program
    )

def convert_to_pm_instrument(instrument: MIDIInstrument):
    pm_instrument = pm.Instrument(instrument.program)
    pm_instrument.notes = [ convert_to_pm_note(n) for n in instrument.notes ]
    return pm_instrument
