"""create_sample_catalog() が参照するダミーVMDファイルを sample_motions/ に生成する。

フェーズ3の時点ではメタデータのみで実ファイルが無くても動作したが、
フェーズ5で実際にファイルをコピーする処理を検証するには実ファイルが必要になる。
ここではモーションの中身を持たない最小限のプレースホルダーVMDを生成する。
"""

from motions.library import create_sample_catalog
from vmd.model import VmdHeader, VmdMotion
from vmd.writer import write_vmd


def main() -> None:
    for entry in create_sample_catalog().all():
        motion = VmdMotion(header=VmdHeader(version=2, model_name=f"ph_{entry.action}"))
        entry.path.parent.mkdir(parents=True, exist_ok=True)
        write_vmd(entry.path, motion)
        print(f"生成しました: {entry.path}")


if __name__ == "__main__":
    main()
