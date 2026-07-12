# mmd-motion-tool

MMD向けのAIモーション生成・編集ツール。文章による指示(例:「元気よく手を振る」)から、
MMDで使えるVMDモーションファイルを生成する。まずはAPIを使わないルールベース版を作る。

## ディレクトリ構成

```
src/vmd/          VMD入出力
src/bones/        ボーン・モーフ知識層
src/rules/        ルールベースの自然言語解析
src/motions/      モーション素材とタグ検索
tests/            テストコード
sample_motions/   検証用の手作りVMDサンプル
```

## セットアップ

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## テストの実行

```bash
pytest
```

## 開発方針

詳細は [CLAUDE.md](CLAUDE.md) を参照。
