from typing import List
import pretty_midi as pm
from collections import defaultdict
from mgenutils.token.Segment import Segment
from mgenutils.midi.MIDIInstrument import MIDIInstrument, convert_pm_instrument
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
        
        return ties + [ EndOfTie() ] + events + [ EndOfSeq() ]

def load_midi(fpath) -> MIDIFile:
    midi = pm.PrettyMIDI(fpath)
    return MIDIFile(
        instruments=[
            convert_pm_instrument(instrument)
            for instrument in midi.instruments
        ]
    )
