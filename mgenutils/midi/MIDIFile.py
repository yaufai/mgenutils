from typing import List, Optional
from collections import defaultdict
import numpy as np
import pretty_midi as pm
from mir_eval.transcription import evaluate
from mgenutils.metrics.MetricsDict import MetricsDict
from mgenutils.token.Segment import Segment
from mgenutils.midi.MIDIInstrument import MIDIInstrument, convert_pm_instrument, convert_to_pm_instrument
from mgenutils.midi.MIDIEvent import MIDIEvent
from mgenutils.token.SemanticToken import Note, Time, NoteOnOff, EndOfSeq, EndOfTie

FrameTime = int
nframes_per_sec = 100

class MIDIFile:
    instruments: List[MIDIInstrument]
    def __init__(self, instruments: List[MIDIInstrument]) -> None:
        self.instruments = instruments

    def get_segment_in_frame(self, start: FrameTime, end: FrameTime) -> Segment:
        """
        MIDIファイルから対象期間内にあるイベントをSemanticTokenの列にして出力する
        """
        time_event_map = defaultdict(list)

        ties   = []
        events = []

        for instrument in self.instruments:
            for note in instrument.notes:
                note.set_scale("frame", nframes_per_sec)
                if note.ends_before(start) or note.begins_after(end):
                    # 対象期間ではない
                    continue
                elif note.begins_before(start) and note.ends_between(start, end):
                    # 対象期間より前に始まり、対象期間内に終わる
                    ties.append(Note(note.pitch))
                elif note.begins_between(start, end) and note.ends_between(start, end):
                    # 対象期間内に収まる
                    time_event_map[note.start - start].append(
                        MIDIEvent(program=instrument.program, onset=True, pitch=note.pitch)
                    )
                    time_event_map[note.end - start].append(
                        MIDIEvent(program=instrument.program, onset=False, pitch=note.pitch)
                    )
                elif note.begins_between(start, end) and note.ends_after(end):
                    # 対象期間内に始まり、対象期間外で終わる
                    time_event_map[note.start - start].append(
                        MIDIEvent(program=instrument.program, onset=True, pitch=note.pitch)
                    )
                elif note.begins_before(start, true_if_simultaneous=False) and note.ends_after(end):
                    # 対象期間を完全に覆いつくす
                    ties.append(Note(note.pitch))
                
        cur_onset = None

        for time in sorted(time_event_map.keys()):
            events.append(Time(time))

            for event in sorted(time_event_map[time]):
                if cur_onset != event.onset:
                    cur_onset = event.onset
                    events.append(NoteOnOff(event.onset))
                events.append(Note(event.pitch))
        
        return Segment(ties + [ EndOfTie() ] + events + [ EndOfSeq() ])
    
    def save(self, fname: str) -> None:
        midi = pm.PrettyMIDI()
        for instrument in self.instruments:
            midi.instruments.append(convert_to_pm_instrument(instrument))
        
        midi.write(fname)
    
    def instrument(self, program: int) -> Optional[MIDIInstrument]:
        instrument = [ i for i in self.instruments if i.program == program ]
        if len(instrument) == 1:
            return instrument[0]
        else:
            return None
    
    def metrics_from(self, midi_ref: "MIDIFile", program: int) -> Optional[MetricsDict]:
        """
        参照先と比較したときの損失を測定する。
        """

        notes_est = self.instrument(program)
        notes_ref = midi_ref.instrument(program)
        
        if notes_est is None or notes_ref is None:
            return None
        
        notes_est = notes_est.notes
        notes_ref = notes_ref.notes
    
        return evaluate(
            np.array([ note.get_interval() for note in notes_ref ]),
            np.array([ note.pitch for note in notes_ref ]),
            np.array([ note.get_interval() for note in notes_est ]),
            np.array([ note.pitch for note in notes_est ])
        )

def load_midi(fpath) -> MIDIFile:
    midi = pm.PrettyMIDI(fpath)
    return MIDIFile(
        instruments=[
            convert_pm_instrument(instrument)
            for instrument in midi.instruments
        ]
    )
