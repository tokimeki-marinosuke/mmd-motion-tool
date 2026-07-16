"""src/bones/morphs.py のテスト。"""

from bones.morphs import CATEGORY_MOUTH, STANDARD_MORPH_CATEGORIES, get_category


def test_requested_morphs_are_present():
    expected = {"まばたき", "笑い", "困る", "あ", "い", "う", "え", "お"}
    assert expected <= STANDARD_MORPH_CATEGORIES.keys()


def test_mouth_vowels_are_categorized_as_mouth():
    for name in ("あ", "い", "う", "え", "お"):
        assert get_category(name) == CATEGORY_MOUTH


def test_get_category_matches_dict():
    for name, category in STANDARD_MORPH_CATEGORIES.items():
        assert get_category(name) == category
