"""src/main.py のテスト。"""

import pytest

from main import run
from vmd.parser import read_vmd


def test_wave_sentence_outputs_matching_vmd(tmp_path):
    output_path = tmp_path / "wave.vmd"
    exit_code = run("元気よく手を振って", output_path=output_path)

    assert exit_code == 0
    assert output_path.exists()


def test_intensity_wording_changes_output_bone_rotation(tmp_path):
    """フェーズ6: 「大きく」と「控えめに」で出力VMDのボーン回転量が変わること。"""
    big_path = tmp_path / "big.vmd"
    small_path = tmp_path / "small.vmd"

    assert run("大きく手を振って", output_path=big_path) == 0
    assert run("控えめに手を振って", output_path=small_path) == 0

    big_motion = read_vmd(big_path)
    small_motion = read_vmd(small_path)

    big_rotation = big_motion.bone_frames[0].rotation
    small_rotation = small_motion.bone_frames[0].rotation

    assert big_rotation != pytest.approx(small_rotation)
    # 「大きく」の方が回転角(wの絶対値が小さいほど回転角は大きい)が大きくなる
    assert abs(big_rotation[3]) < abs(small_rotation[3])


def test_action_without_catalog_entry_reports_not_found_and_does_not_crash(tmp_path, capsys):
    output_path = tmp_path / "nod.vmd"
    exit_code = run("頷いて", output_path=output_path)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "該当するモーションが見つかりませんでした" in captured.out
    assert "nod" in captured.out
    # 出力先に何もコピーされていないこと
    assert not output_path.exists()


def test_unrecognized_sentence_does_not_crash(tmp_path, capsys):
    output_path = tmp_path / "unknown.vmd"
    exit_code = run("今日は天気がいいですね", output_path=output_path)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "文章から動作を読み取れませんでした" in captured.out


def test_bow_sentence_outputs_matching_vmd(tmp_path):
    output_path = tmp_path / "bow.vmd"
    exit_code = run("丁寧にお辞儀する", output_path=output_path)

    assert exit_code == 0
    assert output_path.exists()
