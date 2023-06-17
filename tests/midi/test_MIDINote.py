import unittest
from mgenutils.midi import MIDINote

note1 = MIDINote.MIDINote()
note1.start = 15
note1.end   = 25

class MIDINoteTest_range(unittest.TestCase):
    def test_begins_before_positive_1(self):
        self.assertTrue(note1.begins_before(20))
        
    def test_begins_before_positive_2(self):
        self.assertTrue(note1.begins_before(50))
    
    def test_begins_before_negative_1(self):
        self.assertFalse(note1.begins_before(10))
        
    def test_begins_before_corner_1(self):
        self.assertTrue(note1.begins_before(15, true_if_simultaneous=True))
        
    def test_begins_before_corner_2(self):
        self.assertFalse(note1.begins_before(15, true_if_simultaneous=False))
        
    def test_ends_before_positive_1(self):
        self.assertTrue(note1.ends_before(50))
        
    def test_ends_before_negative_1(self):
        self.assertFalse(note1.ends_before(10))
        
    def test_ends_before_negative_2(self):
        self.assertFalse(note1.ends_before(20))
        
    def test_ends_before_corner_1(self):
        self.assertTrue(note1.ends_before(25, true_if_simultaneous=True))
        
    def test_ends_before_corner_2(self):
        self.assertFalse(note1.ends_before(25, true_if_simultaneous=False))
    
    def test_begins_between_positive_1(self):
        self.assertTrue(note1.begins_between(10, 20))
        
    def test_begins_between_positive_2(self):
        self.assertTrue(note1.begins_between(10, 30))
    
    def test_begins_between_negative_1(self):
        self.assertFalse(note1.begins_between(0, 10))
        
    def test_begins_between_negative_2(self):
        self.assertFalse(note1.begins_between(30, 50))

    def test_ends_between_positive_1(self):
        self.assertTrue(note1.ends_between(20, 30))
        
    def test_ends_between_positive_2(self):
        self.assertTrue(note1.ends_between(10, 30))
    
    def test_ends_between_negative_1(self):
        self.assertFalse(note1.ends_between(10, 20))
        
    def test_ends_between_negative_2(self):
        self.assertFalse(note1.ends_between(30, 50))