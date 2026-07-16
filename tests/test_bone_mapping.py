"""src/bones/mapping.py のテスト。"""

from bones.mapping import STANDARD_BONE_PARENTS, get_children, get_parent


def test_center_is_root():
    assert get_parent("センター") is None


def test_all_parents_are_defined_bones():
    for bone, parent in STANDARD_BONE_PARENTS.items():
        if parent is not None:
            assert parent in STANDARD_BONE_PARENTS, f"{bone} の親 {parent} が未定義"


def test_requested_bones_are_present():
    expected = {
        "センター", "上半身", "下半身", "首", "頭",
        "左肩", "左腕", "左ひじ", "左手首",
        "右肩", "右腕", "右ひじ", "右手首",
        "左足", "左ひざ", "左足首", "左足ＩＫ", "左つま先ＩＫ",
        "右足", "右ひざ", "右足首", "右足ＩＫ", "右つま先ＩＫ",
    }
    assert expected <= STANDARD_BONE_PARENTS.keys()


def test_arm_is_child_of_shoulder():
    assert get_parent("左腕") == "左肩"
    assert get_parent("右腕") == "右肩"
    assert get_parent("左肩") == "上半身"
    assert get_parent("右肩") == "上半身"


def test_get_children_of_center():
    children = get_children("センター")
    assert "上半身" in children
    assert "下半身" in children
    assert "左足ＩＫ" in children
    assert "右足ＩＫ" in children


def test_no_cycles():
    for bone in STANDARD_BONE_PARENTS:
        visited = set()
        current = bone
        while current is not None:
            assert current not in visited, f"循環参照を検出: {bone}"
            visited.add(current)
            current = STANDARD_BONE_PARENTS[current]
