"""日本語の文章から動作タグ・感情タグ・強度を抽出するルールベース解析器。

形態素解析には janome を使用する。MeCabと異なりOS側にバイナリや辞書を別途
インストールする必要がなく、`pip install janome` だけで完結するため、
このプロジェクトの「外部ライブラリは最小限にする」という方針にも合う。

各トークンの基本形(base_form)を使って src/rules/keywords.py のキーワード
辞書と照合することで、「振る」「振ります」「振って」のような活用の違いを
吸収する。
"""

from dataclasses import dataclass

from janome.tokenizer import Tokenizer

from .keywords import (
    ACTION_KEYWORDS,
    BASE_INTENSITY,
    EMOTION_KEYWORDS,
    INTENSITY_KEYWORDS,
    MAX_INTENSITY,
    MIN_INTENSITY,
)

_tokenizer = Tokenizer()


@dataclass
class ParsedMotion:
    """文章から抽出した動作タグ・感情タグ・強度。"""

    action: str | None
    emotion: str | None
    intensity: float

    def to_dict(self) -> dict:
        """{action, emotion, intensity} 形式の辞書に変換する。"""
        return {"action": self.action, "emotion": self.emotion, "intensity": self.intensity}


def parse_sentence(text: str) -> ParsedMotion:
    """日本語の文章を解析し、動作タグ・感情タグ・強度を抽出する。

    action・emotionは、文中で最初に一致したキーワードを採用する。
    intensityはBASE_INTENSITYを基準に、一致した感情・強度キーワードの
    加算量を合計し、[MIN_INTENSITY, MAX_INTENSITY]の範囲に収める。
    """
    action: str | None = None
    emotion: str | None = None
    intensity = BASE_INTENSITY

    for token in _tokenizer.tokenize(text):
        base_form = token.base_form

        if action is None and base_form in ACTION_KEYWORDS:
            action = ACTION_KEYWORDS[base_form]

        if base_form in EMOTION_KEYWORDS:
            keyword_emotion, delta = EMOTION_KEYWORDS[base_form]
            if emotion is None:
                emotion = keyword_emotion
            intensity += delta

        if base_form in INTENSITY_KEYWORDS:
            intensity += INTENSITY_KEYWORDS[base_form]

    intensity = max(MIN_INTENSITY, min(MAX_INTENSITY, intensity))
    return ParsedMotion(action=action, emotion=emotion, intensity=round(intensity, 2))
