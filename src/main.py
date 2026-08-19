"""文章から動作タグを解析し、対応するVMDモーションを出力するコア処理。

処理の流れ:
1. 文章を受け取る
2. src.rules.parser でルールベース解析を行いタグ(action・emotion・intensity)を抽出する
3. src.motions.library のモーションカタログから、タグに最も近いモーションを検索する
4. 該当するVMDファイルを読み込み、intensityに応じてボーンフレームの
   移動量・回転量をスケール調整してから指定パスに書き出す

コマンドラインからの利用は src/cli.py(mmd-motion-tool コマンド)を参照。
"""

from pathlib import Path

from motions.adjust import intensity_to_scale, scale_motion
from motions.library import MotionLibrary, create_sample_catalog
from rules.parser import parse_sentence
from vmd.parser import read_vmd
from vmd.writer import write_vmd


def run(text: str, output_path: Path, catalog: MotionLibrary | None = None) -> int:
    """文章を解析し、該当するVMDをintensityに応じてスケール調整してoutput_pathに書き出す。

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

    motion = read_vmd(entry.path)
    scale = intensity_to_scale(parsed.intensity)
    scaled_motion = scale_motion(motion, scale)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_vmd(output_path, scaled_motion)
    print(f"モーションを出力しました: {output_path} (scale={scale:.2f}倍)")
    return 0
