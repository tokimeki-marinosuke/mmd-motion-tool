"""モーション素材のメタデータ管理。

sample_motions/ 以下に配置するモーションファイルのパスと、動作タイプ(action)・
感情(emotion)・強度(intensity)などのタグを対応付けて管理するカタログを提供する。
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class MotionEntry:
    """1つのモーション素材のメタデータ。"""

    path: Path
    action: str
    emotion: str
    intensity: float = 1.0


class MotionLibrary:
    """モーション素材のカタログ。

    参照するVMDファイルが実際に存在しているかどうかはこのクラスの責務外とし、
    メタデータの登録・検索のみを扱う。
    """

    def __init__(self, entries: list[MotionEntry] | None = None):
        self._entries: list[MotionEntry] = list(entries) if entries else []

    def add(self, entry: MotionEntry) -> None:
        """カタログにモーション素材を1件追加する。"""
        self._entries.append(entry)

    def all(self) -> list[MotionEntry]:
        """登録されている全てのモーション素材を返す。"""
        return list(self._entries)

    def find_by_action(self, action: str) -> list[MotionEntry]:
        """指定したactionタグに一致するモーション素材一覧を返す。"""
        return self.search(action=action)

    def find_by_emotion(self, emotion: str) -> list[MotionEntry]:
        """指定したemotionタグに一致するモーション素材一覧を返す。"""
        return self.search(emotion=emotion)

    def search(self, action: str | None = None, emotion: str | None = None) -> list[MotionEntry]:
        """action・emotionタグで絞り込んだモーション素材一覧を返す。

        指定しなかった条件は絞り込みに使われない。
        """
        results = self._entries
        if action is not None:
            results = [e for e in results if e.action == action]
        if emotion is not None:
            results = [e for e in results if e.emotion == emotion]
        return list(results)

    def find_best_match(self, action: str, emotion: str | None = None) -> MotionEntry | None:
        """action・emotionタグに最も近いモーション素材を1件返す。

        action・emotionの両方に一致するものを優先し、無ければactionのみで
        一致するものを返す。どちらも見つからなければNoneを返す。
        """
        if emotion is not None:
            matches = self.search(action=action, emotion=emotion)
            if matches:
                return matches[0]

        matches = self.search(action=action)
        if matches:
            return matches[0]

        return None


def create_sample_catalog() -> MotionLibrary:
    """動作確認用のダミーメタデータからなるカタログを作成する。

    ここで参照しているVMDファイルは、この時点ではまだ sample_motions/ に
    存在しなくてもよい(このクラスはメタデータの管理のみを担当するため)。
    """
    return MotionLibrary(
        [
            MotionEntry(
                path=Path("sample_motions/wave_happy.vmd"),
                action="wave",
                emotion="happy",
                intensity=0.8,
            ),
            MotionEntry(
                path=Path("sample_motions/bow_polite.vmd"),
                action="bow",
                emotion="polite",
                intensity=0.5,
            ),
            MotionEntry(
                path=Path("sample_motions/turn_back_shy.vmd"),
                action="turn_back",
                emotion="shy",
                intensity=0.3,
            ),
        ]
    )
