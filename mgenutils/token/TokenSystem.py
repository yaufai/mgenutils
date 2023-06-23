import abc
from typing import List, Union
from numpy  import ndarray
from mgenutils.midi.MIDIFile import MIDIFile
from mgenutils.token.Segment import Segment
from mgenutils.token.SemanticToken import SemanticToken

RawToken = int

class TokenSystem(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def encode_token(cls, token: SemanticToken) -> RawToken:
        """
        定義されたトークンを実際に整数値に翻訳する
        """
        pass

    @abc.abstractclassmethod
    def decode_token(cls, token: RawToken) -> SemanticToken:
        """
        整数値から意味上のトークンを復元する
        """
        pass

    @abc.abstractclassmethod
    def encode_segment(cls, segment: Segment) -> ndarray:
        """
        MIDIファイルの一部分を受け取って対応するトークン列に翻訳する
        """
        pass
    
    @classmethod
    def to_ndarray(cls, segment: Segment) -> ndarray:
        return cls.encode_segment(segment)
    
    @abc.abstractclassmethod
    def decode_segment(cls, segment: Union[List[RawToken], ndarray]) -> Segment:
        pass

    @abc.abstractclassmethod
    def decode_segments_to_midi(cls, segments: List[Segment], sec_per_segment: int) -> MIDIFile:
        pass
