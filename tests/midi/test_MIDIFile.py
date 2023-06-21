import unittest
from os.path import dirname, abspath
from mgenutils.midi.MIDIFile import load_midi
from mgenutils.token.Segment import Segment
from mgenutils.token.SemanticToken import EndOfSeq, EndOfTie, Time, Note, NoteOnOff

simple_midi = load_midi(abspath(dirname(__file__)).replace("midi", "resources/simple_1.mid"))

# 単体テストの条件
# (1) まったく関わりのない音符を含む範囲を符号化する
# (2) 範囲より前に始まり範囲内で終わった音符を含む範囲を符号化する
# (3) 範囲内で始まり終わった音符を含む範囲を符号化する
# (4) 範囲内で始まり範囲外で終わった音符を含む範囲を符号化する
# (5) 範囲を完全に包む長さの音符を含む範囲を符号化する

class MIDIFileTest__PianoTokenSystem_get_segment_in_frame(unittest.TestCase):
    def assert_equivalent(self, actual, expected):
        self.assertTrue(
            actual == expected,
            f"\nTwo segments are not equivalent\n* expected: {expected.__repr__()}\n* actual  : {actual.__repr__()}"
        )
    def test_case1_1(self):
        self.assert_equivalent(
            simple_midi.get_segment_in_frame(100, 200),
            Segment([ EndOfTie(), EndOfSeq() ])
        )
    
    def test_case2_1(self):
        self.assert_equivalent(
            simple_midi.get_segment_in_frame(40, 60),
            Segment([ EndOfTie(), Time(10), NoteOnOff(True), Note(48), EndOfSeq() ])
        )
    
    def test_case3_1(self):
        self.assert_equivalent(
            simple_midi.get_segment_in_frame(30, 80),
            Segment([ EndOfTie(), Time(20), NoteOnOff(True), Note(48), Time(45), NoteOnOff(False), Note(48), EndOfSeq() ])
        )
    
    def test_case4_1(self):
        self.assert_equivalent(
            simple_midi.get_segment_in_frame(30, 60),
            Segment([ EndOfTie(), Time(20), NoteOnOff(True), Note(48), EndOfSeq() ])
        )

    def test_case5_1(self):
        self.assert_equivalent(
            simple_midi.get_segment_in_frame(10, 20),
            Segment([ Note(48), EndOfTie(), EndOfSeq() ])
        )
