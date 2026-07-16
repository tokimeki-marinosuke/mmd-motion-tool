"""src/vmd/writer.py のテスト。

最小データでの書き込み単体テストに加え、実際のサンプルモーション
(sample_motions/sample_motion.vmd)を使った読み込み→書き出し→再読み込みの
ラウンドトリップテストを行う。

注意: 元ファイルの文字列フィールドにはヌルバイト以降にMMD由来のゴミバイトが
残っている場合があるが、read_vmd() はそれを切り捨てて文字列化するため、
write_vmd() で書き出したファイルは元ファイルとバイト単位では一致しない
(ゴミバイトの位置がヌルバイトに置き換わる)。そのため、ここでは
「読み込んだデータクラス同士が一致するか」を確認する。
"""

import struct
from pathlib import Path

import pytest

from vmd.model import BoneFrame, MorphFrame, VmdHeader, VmdMotion
from vmd.parser import read_vmd
from vmd.writer import write_vmd

_SAMPLE_PATH = Path(__file__).parent.parent / "sample_motions" / "sample_motion.vmd"

_requires_sample = pytest.mark.skipif(
    not _SAMPLE_PATH.exists(), reason="sample_motions/sample_motion.vmd が見つかりません"
)


def test_write_and_read_minimal_motion(tmp_path):
    motion = VmdMotion(
        header=VmdHeader(version=2, model_name="テストモデル"),
        bone_frames=[
            BoneFrame(
                name="センター",
                frame=0,
                position=(1.0, 2.0, 3.0),
                rotation=(0.0, 0.0, 0.0, 1.0),
                interpolation=bytes(64),
            )
        ],
        morph_frames=[MorphFrame(name="まばたき", frame=5, weight=0.5)],
    )

    out_path = tmp_path / "out.vmd"
    write_vmd(out_path, motion)
    reloaded = read_vmd(out_path)

    assert reloaded == motion


def test_write_version1_header(tmp_path):
    motion = VmdMotion(header=VmdHeader(version=1, model_name="OldModel"))

    out_path = tmp_path / "out.vmd"
    write_vmd(out_path, motion)
    reloaded = read_vmd(out_path)

    assert reloaded.header == motion.header


@_requires_sample
def test_roundtrip_sample_motion(tmp_path):
    """実際のサンプルモーションを読み込み→書き出し→再読み込みし、
    パース結果が完全一致することを確認する(ラウンドトリップテスト)。"""
    original = read_vmd(_SAMPLE_PATH)

    out_path = tmp_path / "roundtrip.vmd"
    write_vmd(out_path, original)
    reloaded = read_vmd(out_path)

    assert reloaded == original


@_requires_sample
def test_roundtrip_preserves_mixed_width_bone_name(tmp_path):
    """半角カナ+全角英字が混在する「ﾈｸﾀｲＩＫ」ボーン名が、
    書き出し→再読み込み後も文字列として完全に保持されることを確認する。"""
    original = read_vmd(_SAMPLE_PATH)
    target_name = "ﾈｸﾀｲＩＫ"
    original_frames = [b for b in original.bone_frames if b.name == target_name]
    assert len(original_frames) > 0  # 前提: サンプルにこのボーンが含まれる

    out_path = tmp_path / "roundtrip.vmd"
    write_vmd(out_path, original)
    reloaded = read_vmd(out_path)

    reloaded_frames = [b for b in reloaded.bone_frames if b.name == target_name]
    assert reloaded_frames == original_frames


@_requires_sample
def test_written_name_field_is_null_padded_not_garbage(tmp_path):
    """元ファイルのボーン名フィールドにはヌルバイト以降にゴミバイト(0xFD等)が
    残っているが、書き出し後のファイルではヌルバイトで正しくパディングされ、
    ゴミバイトが再現されないことを確認する。"""
    original = read_vmd(_SAMPLE_PATH)
    out_path = tmp_path / "roundtrip.vmd"
    write_vmd(out_path, original)

    written = out_path.read_bytes()

    # ヘッダー(シグネチャ30 + モデル名20 = 50バイト、version2前提)の直後が
    # ボーンフレーム件数(uint32)
    assert original.header.version == 2
    offset = 50
    bone_count = struct.unpack("<I", written[offset : offset + 4])[0]
    offset += 4

    record_size = 15 + 4 + 12 + 16 + 64
    target_name = "ﾈｸﾀｲＩＫ"
    found_target = False
    for _ in range(bone_count):
        name_field = written[offset : offset + 15]
        text = name_field.split(b"\x00", 1)[0]
        if text.decode("shift_jis") == target_name:
            found_target = True
            # 文字列本体より後ろは全てヌルバイトであること(ゴミバイトが無いこと)
            assert name_field[len(text) :] == b"\x00" * (15 - len(text))
        offset += record_size

    assert found_target
