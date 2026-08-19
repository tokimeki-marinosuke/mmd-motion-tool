"""create_sample_catalog() が参照するダミーVMDファイルを sample_motions/ に生成する。

フェーズ3の時点ではメタデータのみで実ファイルが無くても動作したが、フェーズ5で
実際にファイルをコピーする処理を、フェーズ6でボーンフレームの回転・移動量を
スケール調整する処理を検証するには実ファイルが必要になる。ここでは各actionを
代表する1件のボーンフレームだけを持つ、最小限のプレースホルダーVMDを生成する。
"""

import math

from motions.library import create_sample_catalog
from vmd.model import BoneFrame, VmdHeader, VmdMotion
from vmd.writer import write_vmd


def _quaternion_from_degrees(axis: tuple[float, float, float], degrees: float) -> tuple[float, float, float, float]:
    """指定した軸(単位ベクトル)・角度(度)からクォータニオン(x, y, z, w)を作る。"""
    half = math.radians(degrees) / 2.0
    sin_half = math.sin(half)
    ax, ay, az = axis
    return (ax * sin_half, ay * sin_half, az * sin_half, math.cos(half))


# action -> (代表ボーン名, 移動量, 回転(軸, 角度))
_PLACEHOLDER_POSES: dict[str, tuple[str, tuple[float, float, float], tuple[tuple[float, float, float], float]]] = {
    "wave": ("右腕", (0.0, 0.0, 0.0), ((0.0, 0.0, 1.0), 45.0)),
    "bow": ("上半身", (0.0, 0.0, 0.0), ((1.0, 0.0, 0.0), 30.0)),
    "turn_back": ("上半身", (0.0, 0.0, 0.0), ((0.0, 1.0, 0.0), 60.0)),
}


def main() -> None:
    for entry in create_sample_catalog().all():
        bone_name, position, (axis, degrees) = _PLACEHOLDER_POSES[entry.action]
        motion = VmdMotion(
            header=VmdHeader(version=2, model_name=f"ph_{entry.action}"),
            bone_frames=[
                BoneFrame(
                    name=bone_name,
                    frame=0,
                    position=position,
                    rotation=_quaternion_from_degrees(axis, degrees),
                    interpolation=bytes(64),
                )
            ],
        )
        entry.path.parent.mkdir(parents=True, exist_ok=True)
        write_vmd(entry.path, motion)
        print(f"生成しました: {entry.path} (bone={bone_name}, {degrees}度)")


if __name__ == "__main__":
    main()
