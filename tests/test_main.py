"""src/main.py のテスト。"""

import pytest

from main import run
from vmd.parser import read_vmd


def test_wave_sentence_outputs_matching_vmd(tmp_path):
    exit_code = run("元気よく手を振って", output_dir=tmp_path)

    assert exit_code == 0
    assert (tmp_path / "wave_happy.vmd").exists()


def test_intensity_wording_changes_output_bone_rotation(tmp_path):
    """フェーズ6: 「大きく」と「控えめに」で出力VMDのボーン回転量が変わること。"""
    big_dir = tmp_path / "big"
    small_dir = tmp_path / "small"

    assert run("大きく手を振って", output_dir=big_dir) == 0
    assert run("控えめに手を振って", output_dir=small_dir) == 0

    big_motion = read_vmd(big_dir / "wave_happy.vmd")
    small_motion = read_vmd(small_dir / "wave_happy.vmd")

    big_rotation = big_motion.bone_frames[0].rotation
    small_rotation = small_motion.bone_frames[0].rotation

    assert big_rotation != pytest.approx(small_rotation)
    # 「大きく」の方が回転角(wの絶対値が小さいほど回転角は大きい)が大きくなる
    assert abs(big_rotation[3]) < abs(small_rotation[3])


def test_action_without_catalog_entry_reports_not_found_and_does_not_crash(tmp_path, capsys):
    exit_code = run("頷いて", output_dir=tmp_path)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "該当するモーションが見つかりませんでした" in captured.out
    assert "nod" in captured.out
    # 出力先に何もコピーされていないこと
    assert list(tmp_path.glob("*.vmd")) == []


def test_unrecognized_sentence_does_not_crash(tmp_path, capsys):
    exit_code = run("今日は天気がいいですね", output_dir=tmp_path)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "文章から動作を読み取れませんでした" in captured.out


def test_bow_sentence_copies_matching_vmd(tmp_path):
    exit_code = run("丁寧にお辞儀する", output_dir=tmp_path)

    assert exit_code == 0
    assert (tmp_path / "bow_polite.vmd").exists()
