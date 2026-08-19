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

## 使い方

`pip install -e .` でインストールすると、`mmd-motion-tool` コマンドが使えるようになる。

```bash
mmd-motion-tool generate "元気よく手を振る" --output output/wave.vmd
```

- 第1引数: モーションを指示する文章(日本語)
- `--output` / `-o`: 出力するVMDファイルのパス(必須)

文章はルールベースで解析され、動作(action)・感情(emotion)・強度(intensity)の
タグに変換される。「もっと」「大きく」「控えめに」のような強度表現を含めると、
出力されるモーションのボーンの移動量・回転量が変化する。

```bash
mmd-motion-tool generate "大きく手を振って" --output output/wave_big.vmd
mmd-motion-tool generate "控えめに手を振って" --output output/wave_small.vmd
```

インストールせずに直接実行する場合は次のようにする。

```bash
python src/cli.py generate "元気よく手を振る" --output output/wave.vmd
```

対応しているaction(モーションカタログに実データがあるもの)は現時点で
`wave`(手を振る)・`bow`(お辞儀)・`turn_back`(振り返る)の3種類。
それ以外のaction(`nod`・`sit`など)はキーワード辞書には存在するが、
モーション素材が未登録のため「該当するモーションが見つかりませんでした」
と表示される。

## 開発方針

詳細は [CLAUDE.md](CLAUDE.md) を参照。
