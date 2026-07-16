"""MMD標準モーフ(表情)名の定義。

モーフには親子関係はないため、カテゴリ(眉・目・口・他)ごとに標準的な
モーフ名を分類した辞書として持たせる。
"""

CATEGORY_EYEBROW = "眉"
CATEGORY_EYE = "目"
CATEGORY_MOUTH = "口"
CATEGORY_OTHER = "他"

# モーフ名 -> カテゴリ
STANDARD_MORPH_CATEGORIES: dict[str, str] = {
    # 眉
    "真面目": CATEGORY_EYEBROW,
    "困る": CATEGORY_EYEBROW,
    "にこり": CATEGORY_EYEBROW,
    "怒り": CATEGORY_EYEBROW,
    "上": CATEGORY_EYEBROW,
    "下": CATEGORY_EYEBROW,
    # 目
    "まばたき": CATEGORY_EYE,
    "笑い": CATEGORY_EYE,
    "ウィンク": CATEGORY_EYE,
    "ウィンク右": CATEGORY_EYE,
    "はぅ": CATEGORY_EYE,
    "じと目": CATEGORY_EYE,
    # 口
    "あ": CATEGORY_MOUTH,
    "い": CATEGORY_MOUTH,
    "う": CATEGORY_MOUTH,
    "え": CATEGORY_MOUTH,
    "お": CATEGORY_MOUTH,
    "にやり": CATEGORY_MOUTH,
    # 他
    "照れ": CATEGORY_OTHER,
    "涙": CATEGORY_OTHER,
}


def get_category(morph_name: str) -> str:
    """指定したモーフのカテゴリ(眉・目・口・他)を返す。"""
    return STANDARD_MORPH_CATEGORIES[morph_name]
