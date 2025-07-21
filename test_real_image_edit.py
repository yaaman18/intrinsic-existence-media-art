#!/usr/bin/env python3
"""
実際の画像を使った現象学的画像編集のテスト
shibuya-1.jpgを使用
"""

import sys
from pathlib import Path
from PIL import Image
import os

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent / "src" / "core"))

try:
    from phenomenological_image_editor import PhenomenologicalImageEditor
except ImportError as e:
    print(f"Error: Could not import image editor: {e}")
    sys.exit(1)


def load_test_image():
    """テスト用画像の読み込み"""
    image_path = Path("examples/images/shibuya-1.jpg")
    
    if not image_path.exists():
        print(f"Error: Image file not found: {image_path}")
        return None
    
    try:
        image = Image.open(image_path)
        print(f"✓ 画像を読み込みました: {image_path}")
        print(f"  - サイズ: {image.size}")
        print(f"  - モード: {image.mode}")
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def save_result(image, filename, description=""):
    """結果画像の保存"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / filename
    try:
        image.save(output_path, quality=95)
        print(f"✓ 編集結果を保存しました: {output_path}")
        if description:
            print(f"  - {description}")
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False


def test_phenomenological_edits():
    """現象学的編集指示のテスト"""
    print("\n=== 渋谷画像での現象学的編集テスト ===")
    
    # 画像読み込み
    original = load_test_image()
    if original is None:
        return
    
    # エディタ初期化
    editor = PhenomenologicalImageEditor()
    
    # 元画像を保存
    save_result(original, "00_original_shibuya.jpg", "元画像")
    
    # テスト1: 霧の密度を高める（現象学オラクルの典型的な指示）
    print("\n1. 霧の密度を高める")
    instruction1 = {
        'action': '霧の密度を高める',
        'location': '画像全体',
        'dimension': ['appearance', 'temporal'],
        'intensity': 0.6
    }
    
    result1 = editor.apply_phenomenological_edit(original, instruction1)
    save_result(result1, "01_fog_effect.jpg", "霧効果 - 内在性の曖昧さを表現")
    
    # テスト2: 時間の流れを表現（動きのブラー）
    print("\n2. 時間の流れを表現")
    instruction2 = {
        'action': '時間の流れと動きを表現する',
        'location': '画像全体',
        'dimension': ['temporal', 'synesthetic'],
        'intensity': 0.5
    }
    
    result2 = editor.apply_phenomenological_edit(original, instruction2)
    save_result(result2, "02_temporal_flow.jpg", "時間の流れ - 動きとテクスチャ")
    
    # テスト3: 存在の境界を曖昧にする
    print("\n3. 存在の境界を曖昧にする")
    instruction3 = {
        'action': '存在の境界を曖昧にし、光の質を変化させる',
        'location': '中央部',
        'dimension': ['ontological', 'appearance'],
        'intensity': 0.7
    }
    
    result3 = editor.apply_phenomenological_edit(original, instruction3)
    save_result(result3, "03_blurred_boundaries.jpg", "存在の境界 - 中央部への集中")
    
    # テスト4: 夜の質感を強調（色温度とコントラスト）
    print("\n4. 夜の都市の質感を強調")
    instruction4 = {
        'action': '夜の都市の質感を強調し、光の温度を調整する',
        'location': '画像全体',
        'dimension': ['synesthetic', 'appearance'],
        'intensity': 0.8
    }
    
    result4 = editor.apply_phenomenological_edit(original, instruction4)
    save_result(result4, "04_night_enhancement.jpg", "夜の質感 - 色温度と質感の調整")
    
    # テスト5: グリッチ効果でデジタル存在を表現
    print("\n5. デジタル存在のグリッチ表現")
    instruction5 = {
        'action': 'デジタル存在の不安定さを表現する',
        'location': '画像全体',
        'dimension': ['ontological', 'temporal'],
        'intensity': 0.4
    }
    
    result5 = editor.apply_phenomenological_edit(original, instruction5)
    save_result(result5, "05_digital_glitch.jpg", "デジタル存在 - グリッチとノイズ")


def test_complex_instruction():
    """複雑な現象学的指示のテスト"""
    print("\n=== 複雑な現象学的指示テスト ===")
    
    original = load_test_image()
    if original is None:
        return
    
    editor = PhenomenologicalImageEditor()
    
    # 内在性オラクルが生成しそうな複雑な指示
    complex_instruction = {
        'action': '霧に包まれた都市の中で、時間の流れが歪み、存在の境界が揺らぎ、光が記憶と現在を交錯させる',
        'location': '多次元的な位置',
        'dimension': ['appearance', 'temporal', 'ontological', 'synesthetic', 'conceptual'],
        'intensity': 0.75,
        'reason': '内的体験の統合的表現として、都市空間における意識の現象学的構造を可視化',
        'integration_with': []
    }
    
    print("複雑な指示:")
    print(f"  アクション: {complex_instruction['action']}")
    print(f"  強度: {complex_instruction['intensity']}")
    print(f"  次元: {', '.join(complex_instruction['dimension'])}")
    
    result = editor.apply_phenomenological_edit(original, complex_instruction)
    save_result(result, "06_complex_phenomenological.jpg", "複雑な現象学的変換")
    
    # 適用されたエフェクトの確認
    if editor.edit_history:
        last_edit = editor.edit_history[-1]
        effects = last_edit.get('effects', [])
        print(f"\n適用されたエフェクト ({len(effects)}個):")
        for i, effect in enumerate(effects, 1):
            print(f"  {i}. {effect['name']} (強度: {effect['intensity']:.2f})")


def test_single_effects():
    """個別エフェクトのテスト"""
    print("\n=== 個別エフェクトテスト ===")
    
    original = load_test_image()
    if original is None:
        return
    
    editor = PhenomenologicalImageEditor()
    
    # 特定エフェクトの単体テスト
    single_effects = [
        ('gaussian_blur', 0.5, "ガウシアンブラー"),
        ('fog_effect', 0.6, "霧効果"),
        ('color_temperature', 0.3, "色温度調整（寒色）"),
        ('vignette', 0.7, "ビネット効果"),
        ('edge_enhance', 0.8, "エッジ強調")
    ]
    
    for i, (effect_name, intensity, description) in enumerate(single_effects, 7):
        print(f"\n{i-6}. {description}")
        result = editor.apply_effect(original, effect_name, intensity)
        filename = f"{i:02d}_{effect_name}.jpg"
        save_result(result, filename, description)


def main():
    """メイン実行関数"""
    print("現象学的画像編集システム - 渋谷画像テスト")
    print("=" * 60)
    
    try:
        # 各テストを実行
        test_phenomenological_edits()
        test_complex_instruction()
        test_single_effects()
        
        print("\n" + "=" * 60)
        print("✅ 全ての画像編集テストが完了しました！")
        print("\n📁 結果画像は 'output' ディレクトリに保存されました")
        print("   - 00_original_shibuya.jpg: 元画像")
        print("   - 01_fog_effect.jpg: 霧効果")
        print("   - 02_temporal_flow.jpg: 時間の流れ")
        print("   - 03_blurred_boundaries.jpg: 存在の境界")
        print("   - 04_night_enhancement.jpg: 夜の質感")
        print("   - 05_digital_glitch.jpg: デジタルグリッチ")
        print("   - 06_complex_phenomenological.jpg: 複雑な現象学的変換")
        print("   - 07-11: 個別エフェクトテスト")
        
    except Exception as e:
        print(f"\n❌ テスト実行中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()