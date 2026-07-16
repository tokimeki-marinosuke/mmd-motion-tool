"""src/bones/mapping.py の定義値が、実際のVMDデータ(sample_motion.vmd)の
ボーン名と整合しているかを確認するテスト。
"""

from pathlib import Path

import pytest

from bones.mapping import STANDARD_BONE_PARENTS
from vmd.parser import read_vmd

_SAMPLE_PATH = Path(__file__).parent.parent / "sample_motions" / "sample_motion.vmd"

pytestmark = pytest.mark.skipif(
    not _SAMPLE_PATH.exists(), reason="sample_motions/sample_motion.vmd が見つかりません"
)


def _real_bone_names() -> set[str]:
    motion = read_vmd(_SAMPLE_PATH)
    return {b.name for b in motion.bone_frames}


def test_all_standard_bones_exist_in_real_motion():
    """mapping.py で定義した全ての標準ボーン(IK系の全角表記・肩ボーンを含む)
    が、実モデルのボーン名とそのまま一致すること。"""
    real_names = _real_bone_names()
    for bone in STANDARD_BONE_PARENTS:
        assert bone in real_names, f"{bone} が実モデルのボーン名に見つかりません"
