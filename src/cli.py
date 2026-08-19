"""mmd-motion-tool のコマンドラインインターフェース。

使い方:

    mmd-motion-tool generate "元気よく手を振る" --output output/wave.vmd

`pip install -e .` でインストールすると `mmd-motion-tool` コマンドとして
使えるようになる(インストールせずに使う場合は `python src/cli.py ...`)。
"""

import argparse
import sys
from pathlib import Path

import main as motion_pipeline


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mmd-motion-tool",
        description="文章による指示からMMD用VMDモーションファイルを生成するツール",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser(
        "generate", help="文章を解析し、対応するVMDモーションファイルを生成する"
    )
    generate_parser.add_argument("text", help="モーションを指示する文章(例: '元気よく手を振る')")
    generate_parser.add_argument(
        "--output", "-o", required=True, type=Path, help="出力するVMDファイルのパス"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        return motion_pipeline.run(args.text, args.output)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
