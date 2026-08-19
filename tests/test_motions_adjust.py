"""src/motions/adjust.py のテスト。"""

import math

import pytest

from motions.adjust import intensity_to_scale, scale_bone_frame, scale_motion
from vmd.model import BoneFrame, MorphFrame, VmdHeader, VmdMotion


def _quaternion_from_degrees(axis, degrees):
    half = math.radians(degrees) / 2.0
    ax, ay, az = axis
    return (ax * math.sin(half), ay * math.sin(half), az * math.sin(half), math.cos(half))


def test_intensity_to_scale_baseline_is_one():
    assert intensity_to_scale(0.5) == pytest.approx(1.0)


def test_intensity_to_scale_matches_guide_examples():
    # 「大きく」(intensity 0.7) は1.2倍、「控えめに」(intensity 0.2) は0.7倍
    assert intensity_to_scale(0.7) == pytest.approx(1.2)
    assert intensity_to_scale(0.2) == pytest.approx(0.7)


def test_scale_bone_frame_scales_position_linearly():
    frame = BoneFrame(
        name="センター", frame=0, position=(1.0, 2.0, 3.0),
        rotation=(0.0, 0.0, 0.0, 1.0), interpolation=bytes(64),
    )
    scaled = scale_bone_frame(frame, 2.0)
    assert scaled.position == pytest.approx((2.0, 4.0, 6.0))


def test_scale_bone_frame_doubles_rotation_angle():
    # Z軸周りに90度の回転を2倍すると、Z軸周りに180度の回転になる
    rotation_90deg_z = _quaternion_from_degrees((0.0, 0.0, 1.0), 90.0)
    frame = BoneFrame(
        name="右腕", frame=0, position=(0.0, 0.0, 0.0),
        rotation=rotation_90deg_z, interpolation=bytes(64),
    )
    scaled = scale_bone_frame(frame, 2.0)
    expected_180deg_z = _quaternion_from_degrees((0.0, 0.0, 1.0), 180.0)
    assert scaled.rotation == pytest.approx(expected_180deg_z, abs=1e-9)


def test_scale_bone_frame_with_scale_one_is_unchanged():
    rotation = _quaternion_from_degrees((0.0, 1.0, 0.0), 45.0)
    frame = BoneFrame(
        name="上半身", frame=0, position=(1.0, 0.0, 0.0),
        rotation=rotation, interpolation=bytes(64),
    )
    scaled = scale_bone_frame(frame, 1.0)
    assert scaled.position == pytest.approx(frame.position)
    assert scaled.rotation == pytest.approx(frame.rotation)


def test_scale_bone_frame_with_zero_rotation_stays_zero():
    frame = BoneFrame(
        name="頭", frame=0, position=(0.0, 0.0, 0.0),
        rotation=(0.0, 0.0, 0.0, 1.0), interpolation=bytes(64),
    )
    scaled = scale_bone_frame(frame, 1.5)
    assert scaled.rotation == pytest.approx((0.0, 0.0, 0.0, 1.0))


def test_scale_motion_scales_all_bone_frames_and_leaves_morphs_untouched():
    motion = VmdMotion(
        header=VmdHeader(version=2, model_name="test"),
        bone_frames=[
            BoneFrame(
                name="右腕", frame=0, position=(2.0, 0.0, 0.0),
                rotation=(0.0, 0.0, 0.0, 1.0), interpolation=bytes(64),
            ),
            BoneFrame(
                name="左腕", frame=0, position=(0.0, 4.0, 0.0),
                rotation=(0.0, 0.0, 0.0, 1.0), interpolation=bytes(64),
            ),
        ],
        morph_frames=[MorphFrame(name="まばたき", frame=0, weight=1.0)],
    )

    scaled = scale_motion(motion, 2.0)

    assert scaled.bone_frames[0].position == pytest.approx((4.0, 0.0, 0.0))
    assert scaled.bone_frames[1].position == pytest.approx((0.0, 8.0, 0.0))
    # モーフフレームはスケール対象外
    assert scaled.morph_frames == motion.morph_frames
    # ヘッダーも変化しない
    assert scaled.header == motion.header
