"""sample_motions/sample_motion.vmd を読み込み、そのまま
output/roundtrip_test.vmd として書き出す動作確認用スクリプト。
"""

from pathlib import Path

from vmd.parser import read_vmd
from vmd.writer import write_vmd

INPUT_PATH = Path("sample_motions/sample_motion.vmd")
OUTPUT_PATH = Path("output/roundtrip_test.vmd")


def main() -> None:
    motion = read_vmd(INPUT_PATH)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_vmd(OUTPUT_PATH, motion)

    print(f"読み込み元: {INPUT_PATH} ({INPUT_PATH.stat().st_size} bytes)")
    print(f"書き出し先: {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size} bytes)")
    print(f"ボーンフレーム数: {len(motion.bone_frames)}")
    print(f"モーフフレーム数: {len(motion.morph_frames)}")


if __name__ == "__main__":
    main()
