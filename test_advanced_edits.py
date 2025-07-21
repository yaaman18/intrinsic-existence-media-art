#!/usr/bin/env python3
"""
より高度な現象学的編集指示のテスト
オラクルシステムが実際に生成するような複雑な指示を模擬
"""

import sys
from pathlib import Path
from PIL import Image

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent / "src" / "core"))

from phenomenological_image_editor import PhenomenologicalImageEditor


def test_oracle_like_instructions():
    """オラクルシステムが生成しそうな指示をテスト"""
    print("現象学的オラクル指示の高度テスト")
    print("=" * 50)
    
    # 画像読み込み
    original = Image.open("examples/images/shibuya-1.jpg")
    editor = PhenomenologicalImageEditor()
    
    # オラクル風の複雑な指示群
    oracle_instructions = [
        {
            "instruction": {
                'action': '夜の街角で光が記憶の断片を織りなす',
                'location': '上部から中央にかけて',
                'dimension': ['appearance', 'temporal', 'conceptual'],
                'intensity': 0.6,
                'reason': '過去と現在の交錯における光の質的変化'
            },
            "filename": "oracle_01_memory_fragments.jpg",
            "description": "記憶の断片 - 光の質的変化"
        },
        {
            "instruction": {
                'action': '都市の喧騒が静寂へと変容し、存在の密度が変化する',
                'location': '境界領域',
                'dimension': ['ontological', 'synesthetic', 'temporal'],
                'intensity': 0.8,
                'reason': '内的静寂における存在密度の現象学的変容'
            },
            "filename": "oracle_02_density_transformation.jpg",
            "description": "存在密度の変容 - 静寂への移行"
        },
        {
            "instruction": {
                'action': '建物の輪郭が溶解し、空間と時間が重層化する',
                'location': '画像全体',
                'dimension': ['ontological', 'temporal', 'spatial'],
                'intensity': 0.7,
                'reason': '空間認識の現象学的解体と再構成'
            },
            "filename": "oracle_03_spatial_dissolution.jpg", 
            "description": "空間の溶解 - 重層化された時空間"
        },
        {
            "instruction": {
                'action': 'ネオンの光が意識の流れとなり、色彩が感情の質感を纏う',
                'location': '中央部',
                'dimension': ['appearance', 'synesthetic', 'conceptual'],
                'intensity': 0.9,
                'reason': '色彩経験の相互感覚的統合'
            },
            "filename": "oracle_04_synesthetic_flow.jpg",
            "description": "相互感覚的な光の流れ - 感情の質感"
        }
    ]
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    for i, test_case in enumerate(oracle_instructions, 1):
        instruction = test_case["instruction"]
        filename = test_case["filename"]
        description = test_case["description"]
        
        print(f"\n{i}. {description}")
        print(f"   指示: {instruction['action']}")
        print(f"   位置: {instruction['location']}")
        print(f"   次元: {', '.join(instruction['dimension'])}")
        print(f"   強度: {instruction['intensity']}")
        
        # 編集実行
        result = editor.apply_phenomenological_edit(original, instruction)
        
        # 保存
        output_path = output_dir / filename
        result.save(output_path, quality=95)
        print(f"   ✓ 保存: {output_path}")
        
        # 適用されたエフェクトの詳細表示
        if editor.edit_history:
            last_edit = editor.edit_history[-1]
            effects = last_edit.get('effects', [])
            print(f"   → 適用エフェクト: {len(effects)}個")
            for effect in effects:
                print(f"     • {effect['name']} (強度: {effect['intensity']:.2f})")


def test_layered_edits():
    """レイヤー化された編集のテスト"""
    print(f"\n{'=' * 50}")
    print("レイヤー化された現象学的編集テスト")
    print("=" * 50)
    
    original = Image.open("examples/images/shibuya-1.jpg")
    editor = PhenomenologicalImageEditor()
    
    # 段階的な編集（進化シミュレーション）
    evolution_steps = [
        {
            'action': '初期状態：都市の物理的現実',
            'location': '画像全体',
            'dimension': ['appearance'],
            'intensity': 0.0  # 元画像のまま
        },
        {
            'action': '第一段階：光の質感が変化し始める',
            'location': '画像全体', 
            'dimension': ['appearance', 'synesthetic'],
            'intensity': 0.3
        },
        {
            'action': '第二段階：時間の流れが知覚される',
            'location': '画像全体',
            'dimension': ['temporal', 'synesthetic'],
            'intensity': 0.5
        },
        {
            'action': '第三段階：存在の境界が曖昧になる',
            'location': '画像全体',
            'dimension': ['ontological', 'temporal'],
            'intensity': 0.7
        },
        {
            'action': '最終段階：意識と環境の統合的体験',
            'location': '画像全体',
            'dimension': ['ontological', 'conceptual', 'synesthetic'],
            'intensity': 0.9
        }
    ]
    
    current_image = original
    output_dir = Path("output")
    
    for i, step in enumerate(evolution_steps):
        print(f"\n段階 {i}: {step['action']}")
        
        if i == 0:
            # 初期状態は元画像をそのまま保存
            filename = f"evolution_{i:02d}_initial.jpg"
        else:
            # 編集適用
            current_image = editor.apply_phenomenological_edit(current_image, step)
            filename = f"evolution_{i:02d}_step{i}.jpg"
        
        # 保存
        output_path = output_dir / filename
        current_image.save(output_path, quality=95)
        print(f"✓ 保存: {output_path}")


def main():
    try:
        test_oracle_like_instructions()
        test_layered_edits()
        
        print(f"\n{'=' * 50}")
        print("🎨 高度な現象学的編集テストが完了しました！")
        print("\n生成された画像:")
        print("  • oracle_01-04: オラクル風の複雑な指示")
        print("  • evolution_00-04: 段階的進化シミュレーション")
        print("\n💫 内在性概念による自律的画像編集のデモンストレーションが成功しました！")
        
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()