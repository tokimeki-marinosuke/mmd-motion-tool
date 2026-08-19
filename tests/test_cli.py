"""src/cli.py のテスト。"""

from cli import main


def test_generate_subcommand_creates_output_file(tmp_path):
    output_path = tmp_path / "wave.vmd"
    exit_code = main(["generate", "元気よく手を振る", "--output", str(output_path)])

    assert exit_code == 0
    assert output_path.exists()


def test_generate_subcommand_short_option(tmp_path):
    output_path = tmp_path / "wave.vmd"
    exit_code = main(["generate", "元気よく手を振る", "-o", str(output_path)])

    assert exit_code == 0
    assert output_path.exists()


def test_generate_without_output_option_errors(capsys):
    try:
        main(["generate", "元気よく手を振る"])
        raised = False
    except SystemExit:
        raised = True

    assert raised  # --output は必須のため、argparseがエラー終了する


def test_missing_command_shows_help_and_returns_error(capsys):
    try:
        main([])
        raised = False
    except SystemExit:
        raised = True

    assert raised  # サブコマンド未指定はargparseの required=True でエラー終了する
