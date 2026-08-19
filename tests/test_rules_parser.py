"""src/rules/parser.py のテスト。

日本語の文章から動作タグ・感情タグ・強度を正しく抽出できるかを、
10種類の入力文で確認する。
"""

import pytest

from rules.parser import parse_sentence


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "元気よく手を振る",
            {"action": "wave", "emotion": "happy", "intensity": 0.8},
        ),
        (
            "少し手を振ってください",
            {"action": "wave", "emotion": None, "intensity": 0.3},
        ),
        (
            "丁寧にお辞儀する",
            {"action": "bow", "emotion": "polite", "intensity": 0.5},
        ),
        (
            "恥ずかしそうに振り返る",
            {"action": "turn_back", "emotion": "shy", "intensity": 0.3},
        ),
        (
            "もっと大きく手を振って",
            {"action": "wave", "emotion": None, "intensity": 0.9},
        ),
        (
            "とても嬉しそうに頷く",
            {"action": "nod", "emotion": "happy", "intensity": 1.0},
        ),
        (
            "控えめに座る",
            {"action": "sit", "emotion": None, "intensity": 0.2},
        ),
        (
            "怒ってお辞儀する",
            {"action": "bow", "emotion": "angry", "intensity": 0.7},
        ),
        (
            "悲しそうに座る",
            {"action": "sit", "emotion": "sad", "intensity": 0.4},
        ),
        (
            "ちょっと恥ずかしそうに振り返ってください",
            {"action": "turn_back", "emotion": "shy", "intensity": 0.1},
        ),
    ],
)
def test_parse_sentence(text, expected):
    assert parse_sentence(text).to_dict() == expected


def test_unrecognized_sentence_has_no_action_or_emotion():
    result = parse_sentence("今日は天気がいいですね")
    assert result.action is None
    assert result.emotion is None
    assert result.intensity == 0.5


def test_intensity_is_clamped_to_max_one():
    # 強度キーワードを重ねても1.0を超えない
    result = parse_sentence("もっと、もっと、とても元気よく大きく手を振って")
    assert result.intensity == 1.0


def test_intensity_is_clamped_to_min_zero():
    # マイナス方向の強度キーワードを重ねても0.0を下回らない
    result = parse_sentence("少しちょっと控えめに小さく悲しそうに座る")
    assert result.intensity == 0.0
