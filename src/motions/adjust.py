"""VMDモーションの動きの大きさ(移動量・回転量)を調整する機能。

src.rules.parser が出力する intensity(0.0〜1.0、基準値0.5)を、ボーン
フレームの移動量・回転量にかけるスケール係数に変換して適用する。
基準値0.5のときscale=1.0(無調整)となるよう、scale = intensity + 0.5 で
変換する。例えば「大きく」(intensity 0.5+0.2=0.7)はscale=1.2倍、
「控えめに」(intensity 0.5-0.3=0.2)はscale=0.7倍になる。
"""

import math
from dataclasses import replace

from vmd.model import BoneFrame, VmdMotion


def intensity_to_scale(intensity: float) -> float:
    """intensity(0.0〜1.0)を移動量・回転量に掛けるスケール係数に変換する。"""
    return intensity + 0.5


def _scale_rotation(
    rotation: tuple[float, float, float, float], scale: float
) -> tuple[float, float, float, float]:
    """クォータニオン(x, y, z, w)が表す回転角をscale倍したクォータニオンを返す。

    クォータニオンの各成分をそのままscale倍すると単位クォータニオンでは
    なくなり不正な回転になってしまうため、回転角と回転軸に分解してから
    角度だけをscale倍し、クォータニオンを再構成する。
    """
    x, y, z, w = rotation
    w_clamped = max(-1.0, min(1.0, w))
    half_angle = math.acos(w_clamped)
    sin_half_angle = math.sqrt(max(0.0, 1.0 - w_clamped * w_clamped))

    if sin_half_angle < 1e-8:
        # 回転がほぼゼロ(単位クォータニオン)の場合、回転軸が定まらないため
        # そのまま返す(何倍してもゼロはゼロ)
        return rotation

    axis = (x / sin_half_angle, y / sin_half_angle, z / sin_half_angle)
    new_half_angle = half_angle * scale
    sin_new_half = math.sin(new_half_angle)
    cos_new_half = math.cos(new_half_angle)
    return (
        axis[0] * sin_new_half,
        axis[1] * sin_new_half,
        axis[2] * sin_new_half,
        cos_new_half,
    )


def scale_bone_frame(frame: BoneFrame, scale: float) -> BoneFrame:
    """1件のボーンフレームの移動量・回転量をscale倍したコピーを返す。"""
    new_position = tuple(v * scale for v in frame.position)
    new_rotation = _scale_rotation(frame.rotation, scale)
    return replace(frame, position=new_position, rotation=new_rotation)


def scale_motion(motion: VmdMotion, scale: float) -> VmdMotion:
    """VmdMotion全体のボーンフレームの移動量・回転量をscale倍したコピーを返す。

    モーフフレームは対象外とする(モーフのウェイトは表情の強さであり、
    ここで言う「動きの大きさ」とは意味が異なるため)。
    """
    new_bone_frames = [scale_bone_frame(f, scale) for f in motion.bone_frames]
    return replace(motion, bone_frames=new_bone_frames)
