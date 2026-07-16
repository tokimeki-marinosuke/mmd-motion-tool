"""VMDファイルの書き出し機能。

docs/vmd_format.md の仕様に基づき、VmdMotionをVMDバイナリに変換する。
parser.py と対称に、カメラ・照明・セルフ影・IK表示フレームは未対応。
"""

import struct
from pathlib import Path

from .model import BoneFrame, MorphFrame, VmdHeader, VmdMotion

_ENCODING = "shift_jis"


class VmdWriteError(Exception):
    """VMDファイルの書き出しに失敗した場合の例外。"""


def _pack_string(text: str, size: int) -> bytes:
    """文字列をShift_JISでエンコードし、ヌルバイトで固定長にパディングする。"""
    raw = text.encode(_ENCODING)
    if len(raw) > size:
        raise VmdWriteError(f"文字列がフィールド長({size}バイト)を超えています: {text!r}")
    return raw + b"\x00" * (size - len(raw))


def _encode_header(header: VmdHeader) -> bytes:
    if header.version == 2:
        signature = "Vocaloid Motion Data 0002"
        name_length = 20
    elif header.version == 1:
        signature = "Vocaloid Motion Data file"
        name_length = 10
    else:
        raise VmdWriteError(f"未対応のバージョンです: {header.version}")

    return _pack_string(signature, 30) + _pack_string(header.model_name, name_length)


def _encode_bone_frames(bone_frames: list[BoneFrame]) -> bytes:
    output = bytearray()
    output += struct.pack("<I", len(bone_frames))
    for bone in bone_frames:
        if len(bone.interpolation) != 64:
            raise VmdWriteError(
                f"補間曲線データは64バイトである必要があります: {len(bone.interpolation)}"
            )
        output += _pack_string(bone.name, 15)
        output += struct.pack("<I", bone.frame)
        output += struct.pack("<3f", *bone.position)
        output += struct.pack("<4f", *bone.rotation)
        output += bone.interpolation
    return bytes(output)


def _encode_morph_frames(morph_frames: list[MorphFrame]) -> bytes:
    output = bytearray()
    output += struct.pack("<I", len(morph_frames))
    for morph in morph_frames:
        output += _pack_string(morph.name, 15)
        output += struct.pack("<I", morph.frame)
        output += struct.pack("<f", morph.weight)
    return bytes(output)


def encode_vmd(motion: VmdMotion) -> bytes:
    """VmdMotionをVMDバイナリデータに変換する。"""
    output = bytearray()
    output += _encode_header(motion.header)
    output += _encode_bone_frames(motion.bone_frames)
    output += _encode_morph_frames(motion.morph_frames)
    return bytes(output)


def write_vmd(path: str | Path, motion: VmdMotion) -> None:
    """VmdMotionをVMDファイルとして書き出す。"""
    Path(path).write_bytes(encode_vmd(motion))
