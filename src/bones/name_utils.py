"""ボーン名・モーフ名の全角/半角表記ゆれを吸収するためのユーティリティ。

MMDモデルによって、IKボーン名を全角(ＩＫ)で書くものと半角(IK)で書くものが
混在する。また「ﾈｸﾀｲ」のような半角カナが使われることもある。Unicode正規化
(NFKC)を使うと、全角英数字は半角に、半角カナは全角カナにそれぞれ統一される
ため、表記ゆれを吸収した比較が可能になる。
"""

import unicodedata


def normalize_bone_name(name: str) -> str:
    """ボーン名を正規化する(NFKC正規化)。

    全角英数字(ＩＫなど)は半角に、半角カナ(ﾈｸﾀｲなど)は全角カナに統一される。
    """
    return unicodedata.normalize("NFKC", name)


def bone_names_equal(name1: str, name2: str) -> bool:
    """正規化した上でボーン名同士が一致するかを判定する。"""
    return normalize_bone_name(name1) == normalize_bone_name(name2)
