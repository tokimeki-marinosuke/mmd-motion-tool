"""文章から動作タグを解析し、対応するVMDモーションを output/ に出力するCLI。

処理の流れ:
1. コマンドライン引数で文章を受け取る
2. src.rules.parser でルールベース解析を行いタグを抽出する
3. src.motions.library のモーションカタログから、タグに最も近いモーションを検索する
4. 該当するVMDファイルをそのまま output/ にコピーする(このフェーズでは編集はしない)
"""

import argparse
import shutil
import sys
from pathlib import Path

from motions.library import MotionLibrary, create_sample_catalog
from rules.parser import parse_sentence

DEFAULT_OUTPUT_DIR = Path("output")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="文章から動作を解析し、対応するVMDモーションをoutput/に出力する"
    )
    parser.add_argument("text", help="モーションを指示する文章(例: '元気よく手を振って')")
    return parser


def run(text: str, output_dir: Path = DEFAULT_OUTPUT_DIR, catalog: MotionLibrary | None = None) -> int:
    """文章を解析し、該当するVMDをoutput_dirにコピーする。

    戻り値は終了コード(成功:0、動作/モーションが見つからない場合:1)。
    """
    if catalog is None:
        catalog = create_sample_catalog()

    parsed = parse_sentence(text)
    print(f"解析結果: action={parsed.action}, emotion={parsed.emotion}, intensity={parsed.intensity}")

    if parsed.action is None:
        print("文章から動作を読み取れませんでした。")
        return 1

    entry = catalog.find_best_match(parsed.action, parsed.emotion)
    if entry is None:
        print(f"該当するモーションが見つかりませんでした(action: {parsed.action})")
        return 1

    if not entry.path.exists():
        print(f"該当するモーションのファイルが見つかりません: {entry.path}")
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / entry.path.name
    shutil.copyfile(entry.path, dest)
    print(f"モーションを出力しました: {dest}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    return run(args.text)


if __name__ == "__main__":
    sys.exit(main())
