"""src/bones/name_utils.py のテスト。"""

from bones.name_utils import bone_names_equal, normalize_bone_name


def test_fullwidth_and_halfwidth_ik_are_equal():
    assert bone_names_equal("左足ＩＫ", "左足IK")
    assert bone_names_equal("右つま先ＩＫ", "右つま先IK")


def test_halfwidth_kana_and_fullwidth_kana_are_equal():
    assert bone_names_equal("ﾈｸﾀｲ", "ネクタイ")


def test_mixed_width_bone_name_normalizes_consistently():
    # 半角カナ+全角英字 と 全角カナ+半角英字 のように書き方が違っても一致する
    assert bone_names_equal("ﾈｸﾀｲＩＫ", "ネクタイIK")


def test_different_bone_names_are_not_equal():
    assert not bone_names_equal("左足ＩＫ", "右足ＩＫ")


def test_normalize_is_idempotent():
    name = "左足ＩＫ"
    once = normalize_bone_name(name)
    twice = normalize_bone_name(once)
    assert once == twice
