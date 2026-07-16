"""src/bones/morphs.py の定義値が、実際のVMDデータ(sample_motion.vmd)の
モーフ名と整合しているかを確認するテスト。
"""

from pathlib import Path

import pytest

from bones.morphs import STANDARD_MORPH_CATEGORIES
from vmd.parser import read_vmd

_SAMPLE_PATH = Path(__file__).parent.parent / "sample_motions" / "sample_motion.vmd"

pytestmark = pytest.mark.skipif(
    not _SAMPLE_PATH.exists(), reason="sample_motions/sample_motion.vmd が見つかりません"
)


def _real_morph_names() -> set[str]:
    motion = read_vmd(_SAMPLE_PATH)
    return {m.name for m in motion.morph_frames}


def test_morphs_used_by_sample_motion_are_categorized():
    """このサンプルモーションが実際に使っているモーフは、'base'を除いて
    全てmorphs.pyでカテゴリ分類されているはず。"""
    real_names = _real_morph_names()
    for name in real_names:
        if name == "base":
            continue
        assert name in STANDARD_MORPH_CATEGORIES, f"{name} がmorphs.pyに未定義"


def test_base_morph_is_not_yet_modeled():
    """既知の注意点: 'base'はPMX/VMDで規約上どのモデルにも存在する基準
    (ニュートラル)モーフだが、表情モーフではないため morphs.py の
    眉/目/口/他のカテゴリには含めていない。"""
    real_names = _real_morph_names()
    assert "base" in real_names
    assert "base" not in STANDARD_MORPH_CATEGORIES
