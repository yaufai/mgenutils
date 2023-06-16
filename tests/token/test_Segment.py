import unittest
from mgenutils.token.Segment import are_equivalent
from mgenutils.token.SemanticToken import EndOfSeq, EndOfTie, Note, Time

empty_segment = [ EndOfTie(), EndOfSeq() ]

class SegmentTest_equivalence(unittest.TestCase):
    def test_are_equivalent_1(self):
        self.assertTrue(are_equivalent(empty_segment, empty_segment))
    
    def test_are_equivalent_shuffled_ties_1(self):
        seg1 = [ Note(48), Note(60), EndOfTie(), EndOfSeq() ]
        seg2 = [ Note(60), Note(48), EndOfTie(), EndOfSeq() ]
        self.assertTrue(are_equivalent(seg1, seg2))

    def test_are_equivalent_shuffled_ties_2(self):
        seg1 = [ Note(48), Note(60), Note(60), EndOfTie(), EndOfSeq() ]
        seg2 = [ Note(60), Note(60), Note(48), EndOfTie(), EndOfSeq() ]
        self.assertTrue(are_equivalent(seg1, seg2))
    
    def test_are_equivalent_shuffled_events_1(self):
        seg1 = [ EndOfTie(), Time(0), Note(48), Note(60), EndOfSeq() ]
        seg2 = [ EndOfTie(), Time(0), Note(60), Note(48), EndOfSeq() ]
        self.assertTrue(are_equivalent(seg1, seg2))

    def test_are_equivalent_shuffled_events_2(self):
        seg1 = [ EndOfTie(), Time(0), Note(48), Note(60), Note(60), EndOfSeq() ]
        seg2 = [ EndOfTie(), Time(0), Note(60), Note(60), Note(48), EndOfSeq() ]
        self.assertTrue(are_equivalent(seg1, seg2))

    def test_are_equivalent_shuffled_events_3(self):
        seg1 = [ EndOfTie(), Time(0), Note(48), Note(60), Note(60), EndOfSeq() ]
        seg2 = [ EndOfTie(), Time(0), Note(60), Note(48), Note(48), EndOfSeq() ]
        self.assertFalse(are_equivalent(seg1, seg2))
    
    def test_are_equivalent_shuffled_events_4(self):
        seg1 = [ EndOfTie(), Time(0), Note(48), Note(60), Note(60), EndOfSeq() ]
        seg2 = [ EndOfTie(), Time(1), Note(48), Note(60), Note(60), EndOfSeq() ]
        self.assertTrue(are_equivalent(seg1, seg2))
        
if __name__ == "__main__":
    unittest.main()