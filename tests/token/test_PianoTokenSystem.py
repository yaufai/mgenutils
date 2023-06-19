import unittest
from mgenutils.token.SemanticToken import EndOfSeq, EndOfTie, Note, Time, Padding, NoteOnOff
from mgenutils.token.PianoTokenSystem import PianoTokenSystem

class PianoTokenSystemTest_encode(unittest.TestCase):
    def test_encode_padding_1(self):
        self.assertEqual(PianoTokenSystem.encode_token(Padding()), 0)
    
    def test_encode_endofseq_1(self):
        self.assertEqual(PianoTokenSystem.encode_token(EndOfSeq()), 1)

    def test_encode_endoftie_1(self):
        self.assertEqual(PianoTokenSystem.encode_token(EndOfTie()), 2)
        
    def test_encode_pitch_1(self):
        self.assertEqual(PianoTokenSystem.encode_token(Note(0)), 3)

    def test_encode_pitch_2(self):
        self.assertEqual(PianoTokenSystem.encode_token(Note(48)), 51)
    
    def test_encode_onset_1(self):
        self.assertEqual(PianoTokenSystem.encode_token(NoteOnOff(False)), 131)

    def test_encode_onset_2(self):
        self.assertEqual(PianoTokenSystem.encode_token(NoteOnOff(True)), 132)
    
    def test_encode_time_1(self):
        self.assertEqual(PianoTokenSystem.encode_token(Time(0)), 133)
    
    def test_encode_time_1(self):
        self.assertEqual(PianoTokenSystem.encode_token(Time(25)), 158)
    
        
        
class PianoTokenSystemTest_decode(unittest.TestCase):
    def test_decode_padding_1(self):
        self.assertEqual(PianoTokenSystem.decode_token(0), Padding())
    
    def test_decode_endofseq_1(self):
        self.assertEqual(PianoTokenSystem.decode_token(1), EndOfSeq())

    def test_decode_endoftie_1(self):
        self.assertEqual(PianoTokenSystem.decode_token(2), EndOfTie())
        
    def test_decode_pitch_1(self):
        self.assertEqual(PianoTokenSystem.decode_token(3), Note(0))

    def test_decode_pitch_2(self):
        self.assertEqual(PianoTokenSystem.decode_token(51), Note(48))
    
    def test_decode_onset_1(self):
        self.assertEqual(PianoTokenSystem.decode_token(131), NoteOnOff(False))

    def test_decode_onset_2(self):
        self.assertEqual(PianoTokenSystem.decode_token(132), NoteOnOff(True))
    
    def test_decode_time_1(self):
        self.assertEqual(PianoTokenSystem.decode_token(133), Time(0))
    
    def test_decode_time_1(self):
        self.assertEqual(PianoTokenSystem.decode_token(158), Time(25))