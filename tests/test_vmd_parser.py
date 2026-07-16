"""src/vmd/parser.py のテスト。

実際のMMD配布VMDを使った検証はフェーズ1-cで行うため、ここではdocs/vmd_format.md
の仕様通りに組み立てた最小のバイナリデータを使って解析結果を検証する。
"""

import struct

import pytest

from vmd.parser import VmdParseError, parse_vmd


def _pad(text: str, size: int) -> bytes:
    """文字列をShift_JISでエンコードし、ヌルバイトで固定長にパディングする。"""
    raw = text.encode("shift_jis")
    assert len(raw) <= size
    return raw + b"\x00" * (size - len(raw))


def _build_sample_vmd_bytes() -> bytes:
    data = bytearray()
    data += _pad("Vocaloid Motion Data 0002", 30)
    data += _pad("テストモデル", 20)

    # ボーンフレーム1件
    data += struct.pack("<I", 1)
    data += _pad("センター", 15)
    data += struct.pack("<I", 0)  # frame
    data += struct.pack("<3f", 1.0, 2.0, 3.0)  # position
    data += struct.pack("<4f", 0.0, 0.0, 0.0, 1.0)  # rotation (quaternion)
    data += bytes(64)  # interpolation(物理ON相当のゼロ埋め)

    # モーフフレーム1件
    data += struct.pack("<I", 1)
    data += _pad("まばたき", 15)
    data += struct.pack("<I", 5)  # frame
    data += struct.pack("<f", 0.5)  # weight

    return bytes(data)


def test_parse_header():
    motion = parse_vmd(_build_sample_vmd_bytes())
    assert motion.header.version == 2
    assert motion.header.model_name == "テストモデル"


def test_parse_bone_frame():
    motion = parse_vmd(_build_sample_vmd_bytes())
    assert len(motion.bone_frames) == 1
    bone = motion.bone_frames[0]
    assert bone.name == "センター"
    assert bone.frame == 0
    assert bone.position == pytest.approx((1.0, 2.0, 3.0))
    assert bone.rotation == pytest.approx((0.0, 0.0, 0.0, 1.0))
    assert len(bone.interpolation) == 64


def test_parse_morph_frame():
    motion = parse_vmd(_build_sample_vmd_bytes())
    assert len(motion.morph_frames) == 1
    morph = motion.morph_frames[0]
    assert morph.name == "まばたき"
    assert morph.frame == 5
    assert morph.weight == pytest.approx(0.5)


def test_parse_version1_header():
    data = bytearray()
    data += _pad("Vocaloid Motion Data file", 30)
    data += _pad("OldModel", 10)
    data += struct.pack("<I", 0)  # ボーンフレーム0件
    data += struct.pack("<I", 0)  # モーフフレーム0件

    motion = parse_vmd(bytes(data))
    assert motion.header.version == 1
    assert motion.header.model_name == "OldModel"


def test_unknown_signature_raises():
    data = _pad("Not A Valid VMD Signature!!!!", 30)
    with pytest.raises(VmdParseError):
        parse_vmd(data)


def test_truncated_file_raises():
    data = _pad("Vocaloid Motion Data 0002", 30)  # モデル名以降が存在しない
    with pytest.raises(VmdParseError):
        parse_vmd(data)
