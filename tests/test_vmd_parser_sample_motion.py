"""実際にMMD公式が配布しているサンプルモーション(軽いダンス)を使った検証。

フェーズ1-c: 合成データだけでなく、実在のVMDファイルに対してもパーサーが
正しく動作することを確認する。
"""

from pathlib import Path

import pytest

from vmd.parser import read_vmd

_SAMPLE_PATH = Path(__file__).parent.parent / "sample_motions" / "sample_motion.vmd"

pytestmark = pytest.mark.skipif(
    not _SAMPLE_PATH.exists(), reason="sample_motions/sample_motion.vmd が見つかりません"
)


def test_read_sample_motion_header():
    motion = read_vmd(_SAMPLE_PATH)
    assert motion.header.version == 2
    assert motion.header.model_name == "初音ミク(メタル服)"


def test_read_sample_motion_bone_frames():
    motion = read_vmd(_SAMPLE_PATH)
    assert len(motion.bone_frames) == 3655
    # 全ボーンフレームがフレーム番号0以上、補間曲線64バイトを持つこと
    for bone in motion.bone_frames:
        assert bone.frame >= 0
        assert len(bone.interpolation) == 64
    # 実際に登場するボーン名の一例(センター・上半身)が含まれていること
    bone_names = {bone.name for bone in motion.bone_frames}
    assert "センター" in bone_names
    assert "上半身" in bone_names


def test_read_sample_motion_morph_frames():
    motion = read_vmd(_SAMPLE_PATH)
    assert len(motion.morph_frames) == 256
    morph_names = {morph.name for morph in motion.morph_frames}
    # まばたきや表情モーフが含まれていること
    assert "まばたき" in morph_names
    assert "笑い" in morph_names
