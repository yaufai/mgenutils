import unittest
from mgenutils.token.Segment import Segment
from mgenutils.token.SemanticToken import EndOfSeq, EndOfTie, Note, NoteOnOff, Time

empty_segment = Segment([ EndOfTie(), EndOfSeq() ])

class SegmentTest_equivalence(unittest.TestCase):
    def test_are_equivalent_1(self):
        self.assertTrue(empty_segment == empty_segment)
    
    def test_are_equivalent_shuffled_ties_1(self):
        seg1 = Segment([ Note(48), Note(60), EndOfTie(), EndOfSeq() ])
        seg2 = Segment([ Note(60), Note(48), EndOfTie(), EndOfSeq() ])
        self.assertTrue(seg1 == seg2)

    def test_are_equivalent_shuffled_ties_2(self):
        seg1 = Segment([ Note(48), Note(60), Note(60), EndOfTie(), EndOfSeq() ])
        seg2 = Segment([ Note(60), Note(60), Note(48), EndOfTie(), EndOfSeq() ])
        self.assertTrue(seg1 == seg2)
    
    def test_are_equivalent_shuffled_events_1(self):
        seg1 = Segment([ EndOfTie(), Time(0), NoteOnOff(True), Note(48), Note(60), EndOfSeq() ])
        seg2 = Segment([ EndOfTie(), Time(0), NoteOnOff(True), Note(60), Note(48), EndOfSeq() ])
        self.assertTrue(seg1 == seg2)

    def test_are_equivalent_shuffled_events_2(self):
        seg1 = Segment([ EndOfTie(), Time(0), NoteOnOff(True), Note(48), Note(60), Note(60), EndOfSeq() ])
        seg2 = Segment([ EndOfTie(), Time(0), NoteOnOff(True), Note(60), Note(60), Note(48), EndOfSeq() ])
        self.assertTrue(seg1 == seg2)

    def test_are_equivalent_shuffled_events_3(self):
        seg1 = Segment([ EndOfTie(), Time(0), NoteOnOff(True), Note(48), Note(60), Note(60), EndOfSeq() ])
        seg2 = Segment([ EndOfTie(), Time(0), NoteOnOff(True), Note(60), Note(48), Note(48), EndOfSeq() ])
        self.assertFalse(seg1 == seg2)
    
    def test_are_equivalent_shuffled_events_4(self):
        seg1 = Segment([ EndOfTie(), Time(0), NoteOnOff(True), Note(48), Note(60), Note(60), EndOfSeq() ])
        seg2 = Segment([ EndOfTie(), Time(1), NoteOnOff(True), Note(48), Note(60), Note(60), EndOfSeq() ])
        self.assertFalse(seg1 == seg2)
        