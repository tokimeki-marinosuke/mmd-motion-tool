"""VMDデータを表すデータクラス群。"""

from dataclasses import dataclass, field


@dataclass
class VmdHeader:
    """VMDファイルのヘッダー情報。"""

    version: int  # 1 または 2
    model_name: str


@dataclass
class BoneFrame:
    """ボーンフレーム1件分のデータ。"""

    name: str
    frame: int
    position: tuple[float, float, float]
    rotation: tuple[float, float, float, float]  # クォータニオン (x, y, z, w)
    interpolation: bytes  # 64バイトの補間曲線データ(未解釈のまま保持)


@dataclass
class MorphFrame:
    """モーフ(表情)フレーム1件分のデータ。"""

    name: str
    frame: int
    weight: float


@dataclass
class VmdMotion:
    """VMDファイル全体(ボーン・モーフフレームのみ)を表す。"""

    header: VmdHeader
    bone_frames: list[BoneFrame] = field(default_factory=list)
    morph_frames: list[MorphFrame] = field(default_factory=list)
