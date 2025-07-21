#!/usr/bin/env python3
"""
現象学的画像編集システムのテストスクリプト
"""

import sys
from pathlib import Path
from PIL import Image
import json

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent / "src" / "core"))

try:
    from phenomenological_image_editor import PhenomenologicalImageEditor, EffectLibrary, MaskGenerator
except ImportError as e:
    print(f"Error: Could not import image editor: {e}")
    print("Make sure the image editor is properly installed.")
    sys.exit(1)


def create_test_image() -> Image.Image:
    """テスト用の画像を作成"""
    # グラデーション背景の作成
    width, height = 800, 600
    image = Image.new('RGB', (width, height))
    pixels = []
    
    for y in range(height):
        for x in range(width):
            # 虹色のグラデーション
            r = int(255 * x / width)
            g = int(255 * y / height)
            b = int(255 * (1 - x / width) * (1 - y / height))
            pixels.append((r, g, b))
    
    image.putdata(pixels)
    return image


def test_basic_effects():
    """基本エフェクトのテスト"""
    print("\n=== 基本エフェクトテスト ===")
    
    editor = PhenomenologicalImageEditor()
    test_img = create_test_image()
    
    effects_to_test = [
        ('gaussian_blur', 0.6),
        ('motion_blur', 0.5),
        ('brightness_adjust', 0.7),
        ('contrast_adjust', 0.6),
        ('color_adjust', 0.8),
        ('color_temperature', 0.4),
        ('add_noise', 0.3),
        ('edge_enhance', 0.5),
        ('vignette', 0.4),
        ('chromatic_aberration', 0.3),
        ('fog_effect', 0.5),
        ('glitch_effect', 0.3),
        ('texture_overlay', 0.4)
    ]
    
    for effect_name, intensity in effects_to_test:
        try:
            result = editor.apply_effect(test_img, effect_name, intensity)
            print(f"✓ {effect_name}: 正常に適用されました")
        except Exception as e:
            print(f"✗ {effect_name}: エラーが発生しました - {e}")


def test_mask_generation():
    """マスク生成のテスト"""
    print("\n=== マスク生成テスト ===")
    
    mask_gen = MaskGenerator()
    size = (800, 600)
    
    masks_to_test = [
        ('full_mask', {}),
        ('center_mask', {'radius_ratio': 0.5, 'feather': 0.2}),
        ('edge_mask', {'thickness': 0.3}),
        ('gradient_mask', {'direction': 'vertical', 'reverse': False}),
        ('gradient_mask', {'direction': 'horizontal', 'reverse': True}),
        ('gradient_mask', {'direction': 'radial', 'reverse': False})
    ]
    
    for mask_name, params in masks_to_test:
        try:
            mask_func = getattr(mask_gen, mask_name)
            mask = mask_func(size, **params)
            print(f"✓ {mask_name}: マスクが生成されました (shape: {mask.shape})")
        except Exception as e:
            print(f"✗ {mask_name}: エラーが発生しました - {e}")


def test_phenomenological_instructions():
    """現象学的編集指示のテスト"""
    print("\n=== 現象学的編集指示テスト ===")
    
    editor = PhenomenologicalImageEditor()
    test_img = create_test_image()
    
    instructions = [
        {
            'action': '霧の密度を高める',
            'location': '画像全体',
            'dimension': ['appearance', 'temporal'],
            'intensity': 0.6
        },
        {
            'action': '明度を上げる',
            'location': '中央部',
            'dimension': ['appearance'],
            'intensity': 0.5
        },
        {
            'action': 'ぼかしを適用',
            'location': '境界領域',
            'dimension': ['appearance', 'temporal'],
            'intensity': 0.4
        },
        {
            'action': 'コントラストを強化',
            'location': '上部',
            'dimension': ['appearance'],
            'intensity': 0.7
        },
        {
            'action': 'グリッチ効果を追加',
            'location': '画像全体',
            'dimension': ['temporal', 'ontological'],
            'intensity': 0.3
        }
    ]
    
    for i, instruction in enumerate(instructions, 1):
        try:
            result = editor.apply_phenomenological_edit(test_img, instruction)
            print(f"✓ 指示 {i}: '{instruction['action']}' が正常に適用されました")
        except Exception as e:
            print(f"✗ 指示 {i}: エラーが発生しました - {e}")


def test_multiple_effects():
    """複数エフェクトの適用テスト"""
    print("\n=== 複数エフェクト適用テスト ===")
    
    editor = PhenomenologicalImageEditor()
    test_img = create_test_image()
    
    # シンプルな複数エフェクト
    effects1 = [
        {'name': 'gaussian_blur', 'intensity': 0.3},
        {'name': 'brightness_adjust', 'intensity': 0.6},
        {'name': 'vignette', 'intensity': 0.4}
    ]
    
    # マスク付きの複数エフェクト
    effects2 = [
        {
            'name': 'fog_effect',
            'intensity': 0.5,
            'mask': {'type': 'center', 'radius': 0.6, 'feather': 0.3}
        },
        {
            'name': 'edge_enhance',
            'intensity': 0.7,
            'mask': {'type': 'edge', 'thickness': 0.2}
        }
    ]
    
    try:
        result1 = editor.apply_multiple_effects(test_img, effects1)
        print("✓ シンプルな複数エフェクト: 正常に適用されました")
    except Exception as e:
        print(f"✗ シンプルな複数エフェクト: エラーが発生しました - {e}")
    
    try:
        result2 = editor.apply_multiple_effects(test_img, effects2)
        print("✓ マスク付き複数エフェクト: 正常に適用されました")
    except Exception as e:
        print(f"✗ マスク付き複数エフェクト: エラーが発生しました - {e}")


def test_edit_history():
    """編集履歴のテスト"""
    print("\n=== 編集履歴テスト ===")
    
    editor = PhenomenologicalImageEditor()
    test_img = create_test_image()
    
    # いくつかの編集を実行
    instructions = [
        {
            'action': '霧の密度を高める',
            'location': '画像全体',
            'dimension': ['appearance'],
            'intensity': 0.5
        },
        {
            'action': '明度調整',
            'location': '中央部',
            'dimension': ['appearance'],
            'intensity': 0.6
        }
    ]
    
    for instruction in instructions:
        editor.apply_phenomenological_edit(test_img, instruction)
    
    # 履歴の保存と読み込みテスト
    try:
        history_file = "/tmp/test_edit_history.json"
        editor.save_edit_history(history_file)
        print(f"✓ 編集履歴の保存: 成功 ({len(editor.edit_history)} 件の編集)")
        
        # 新しいエディタインスタンスで履歴を読み込み
        new_editor = PhenomenologicalImageEditor()
        new_editor.load_edit_history(history_file)
        print(f"✓ 編集履歴の読み込み: 成功 ({len(new_editor.edit_history)} 件の編集)")
        
    except Exception as e:
        print(f"✗ 編集履歴テスト: エラーが発生しました - {e}")


def test_realistic_oracle_scenario():
    """現実的なオラクルシナリオのテスト"""
    print("\n=== 現実的なオラクルシナリオテスト ===")
    
    editor = PhenomenologicalImageEditor()
    test_img = create_test_image()
    
    # オラクルシステムからの複雑な指示をシミュレート
    oracle_instruction = {
        'action': '霧の密度を高め、時間の流れを表現し、存在の境界を曖昧にする',
        'location': '多次元的な位置',
        'dimension': ['appearance', 'temporal', 'ontological', 'synesthetic'],
        'intensity': 0.7,
        'reason': '内的体験の統合的な表現',
        'integration_with': []
    }
    
    try:
        # 複雑な指示を処理
        result = editor.apply_phenomenological_edit(test_img, oracle_instruction)
        print("✓ 複雑なオラクル指示: 正常に解析・適用されました")
        
        # 適用されたエフェクトの確認
        if editor.edit_history:
            last_edit = editor.edit_history[-1]
            effects = last_edit.get('effects', [])
            print(f"  - 適用されたエフェクト数: {len(effects)}")
            for effect in effects:
                print(f"    • {effect['name']} (強度: {effect['intensity']:.2f})")
                
    except Exception as e:
        print(f"✗ 複雑なオラクル指示: エラーが発生しました - {e}")


def performance_test():
    """パフォーマンステスト"""
    print("\n=== パフォーマンステスト ===")
    
    import time
    
    editor = PhenomenologicalImageEditor()
    test_img = create_test_image()
    
    # 大きな画像でのテスト
    large_img = test_img.resize((1920, 1080))
    
    start_time = time.time()
    
    instruction = {
        'action': '霧の密度を高める',
        'location': '画像全体',
        'dimension': ['appearance', 'temporal'],
        'intensity': 0.5
    }
    
    result = editor.apply_phenomenological_edit(large_img, instruction)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"✓ 大きな画像 (1920x1080) の処理時間: {processing_time:.2f}秒")
    
    if processing_time < 5.0:
        print("  → パフォーマンス: 良好")
    elif processing_time < 10.0:
        print("  → パフォーマンス: 普通")
    else:
        print("  → パフォーマンス: 改善が必要")


def main():
    """メイン実行関数"""
    print("現象学的画像編集システム - 包括的テスト")
    print("=" * 50)
    
    try:
        # 各テストを実行
        test_basic_effects()
        test_mask_generation()
        test_phenomenological_instructions()
        test_multiple_effects()
        test_edit_history()
        test_realistic_oracle_scenario()
        performance_test()
        
        print("\n" + "=" * 50)
        print("✅ 全てのテストが完了しました！")
        print("\n利用可能なエフェクト一覧:")
        
        # 利用可能なエフェクトの一覧表示
        effect_methods = [method for method in dir(EffectLibrary) 
                         if not method.startswith('_') and callable(getattr(EffectLibrary, method))]
        
        for i, effect in enumerate(effect_methods, 1):
            print(f"  {i:2d}. {effect}")
        
        print(f"\n合計 {len(effect_methods)} 種類のエフェクトが利用可能です。")
        
    except Exception as e:
        print(f"\n❌ テスト実行中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()