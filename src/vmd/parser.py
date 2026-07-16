"""VMDファイルの読み込み機能。

docs/vmd_format.md の仕様に基づき、VMDバイナリを解析してPythonのデータクラスに
変換する。カメラ・照明・セルフ影・IK表示フレームは未対応(後続フェーズで対応)。
"""

import struct
from pathlib import Path

from .model import BoneFrame, MorphFrame, VmdHeader, VmdMotion

_ENCODING = "shift_jis"


class VmdParseError(Exception):
    """VMDファイルの解析に失敗した場合の例外。"""


class _Reader:
    """バイト列を先頭から順に読み進めるための小さなヘルパー。"""

    def __init__(self, data: bytes):
        self._data = data
        self._offset = 0

    def read_bytes(self, size: int) -> bytes:
        if self._offset + size > len(self._data):
            raise VmdParseError(
                f"ファイルの終端に達しました(offset={self._offset}, size={size})"
            )
        chunk = self._data[self._offset : self._offset + size]
        self._offset += size
        return chunk

    def read_string(self, size: int) -> str:
        raw = self.read_bytes(size)
        # ヌルバイト以降はMMDが残すゴミデータの可能性があるため切り捨てる
        return raw.split(b"\x00", 1)[0].decode(_ENCODING, errors="replace")

    def read_uint32(self) -> int:
        return struct.unpack("<I", self.read_bytes(4))[0]

    def read_float(self) -> float:
        return struct.unpack("<f", self.read_bytes(4))[0]

    def read_floats(self, count: int) -> tuple:
        return struct.unpack(f"<{count}f", self.read_bytes(4 * count))


def _parse_header(reader: _Reader) -> VmdHeader:
    signature = reader.read_string(30)
    if signature == "Vocaloid Motion Data 0002":
        version = 2
        name_length = 20
    elif signature == "Vocaloid Motion Data file":
        version = 1
        name_length = 10
    else:
        raise VmdParseError(f"未対応のVMDシグネチャです: {signature!r}")

    model_name = reader.read_string(name_length)
    return VmdHeader(version=version, model_name=model_name)


def _parse_bone_frames(reader: _Reader) -> list[BoneFrame]:
    count = reader.read_uint32()
    frames = []
    for _ in range(count):
        name = reader.read_string(15)
        frame = reader.read_uint32()
        position = reader.read_floats(3)
        rotation = reader.read_floats(4)
        interpolation = reader.read_bytes(64)
        frames.append(
            BoneFrame(
                name=name,
                frame=frame,
                position=position,
                rotation=rotation,
                interpolation=interpolation,
            )
        )
    return frames


def _parse_morph_frames(reader: _Reader) -> list[MorphFrame]:
    count = reader.read_uint32()
    frames = []
    for _ in range(count):
        name = reader.read_string(15)
        frame = reader.read_uint32()
        weight = reader.read_float()
        frames.append(MorphFrame(name=name, frame=frame, weight=weight))
    return frames


def parse_vmd(data: bytes) -> VmdMotion:
    """VMDバイナリデータを解析し、VmdMotionを返す。"""
    reader = _Reader(data)
    header = _parse_header(reader)
    bone_frames = _parse_bone_frames(reader)
    morph_frames = _parse_morph_frames(reader)
    return VmdMotion(header=header, bone_frames=bone_frames, morph_frames=morph_frames)


def read_vmd(path: str | Path) -> VmdMotion:
    """VMDファイルを読み込み、VmdMotionを返す。"""
    data = Path(path).read_bytes()
    return parse_vmd(data)
