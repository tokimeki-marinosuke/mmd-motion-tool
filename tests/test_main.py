"""src/main.py のテスト。"""

from main import run


def test_wave_sentence_copies_matching_vmd(tmp_path):
    exit_code = run("元気よく手を振って", output_dir=tmp_path)

    assert exit_code == 0
    assert (tmp_path / "wave_happy.vmd").exists()


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
