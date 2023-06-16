import abc
from typing import List
from mgenutils.token.Segment import Segment
from mgenutils.token.SemanticToken import SemanticToken

RawToken = int

class TokenSystem(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def encode_token(token: SemanticToken) -> RawToken:
        """
        定義されたトークンを実際に整数値に翻訳する
        """
        pass

    @abc.abstractclassmethod
    def decode_token(token: RawToken) -> SemanticToken:
        """
        整数値から意味上のトークンを復元する
        """
        pass

    @abc.abstractmethod
    def encode_segment(segment: Segment) -> List[RawToken]:
        """
        MIDIファイルの一部分を受け取って対応するトークン列に翻訳する
        """
        pass
    
