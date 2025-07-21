#!/usr/bin/env python3
"""
RGB色彩編集機能の包括的テスト
shibuya-1.jpgを使用したRGB/色彩操作のデモンストレーション
"""

import sys
from pathlib import Path
from PIL import Image

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent / "src" / "core"))

from phenomenological_image_editor import PhenomenologicalImageEditor, EffectLibrary


def load_test_image():
    """テスト画像の読み込み"""
    image_path = Path("examples/images/shibuya-1.jpg")
    
    if not image_path.exists():
        print(f"❌ 画像ファイルが見つかりません: {image_path}")
        return None
    
    try:
        image = Image.open(image_path)
        print(f"✅ 画像を読み込みました: {image_path}")
        print(f"   サイズ: {image.size[0]} x {image.size[1]} pixels")
        return image
    except Exception as e:
        print(f"❌ 画像読み込みエラー: {e}")
        return None


def save_result(image, filename, description=""):
    """結果画像の保存"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / filename
    try:
        image.save(output_path, quality=95)
        print(f"✅ 保存完了: {output_path}")
        if description:
            print(f"   {description}")
        return True
    except Exception as e:
        print(f"❌ 保存エラー: {e}")
        return False


def test_basic_rgb_operations():
    """基本的なRGB操作テスト"""
    print("\n🎨 基本的なRGB操作テスト")
    print("=" * 50)
    
    original = load_test_image()
    if original is None:
        return
    
    save_result(original, "rgb_00_original.jpg", "元画像")
    
    # RGB個別チャンネル調整テスト
    rgb_tests = [
        # (r_factor, g_factor, b_factor, filename, description)
        (1.5, 1.0, 1.0, "rgb_01_red_boost.jpg", "赤チャンネル強化"),
        (0.7, 1.0, 1.0, "rgb_02_red_reduce.jpg", "赤チャンネル減少"),
        (1.0, 1.5, 1.0, "rgb_03_green_boost.jpg", "緑チャンネル強化"),
        (1.0, 0.7, 1.0, "rgb_04_green_reduce.jpg", "緑チャンネル減少"),
        (1.0, 1.0, 1.5, "rgb_05_blue_boost.jpg", "青チャンネル強化"),
        (1.0, 1.0, 0.7, "rgb_06_blue_reduce.jpg", "青チャンネル減少"),
        (1.3, 0.8, 0.9, "rgb_07_warm_tone.jpg", "暖色調整（赤↑緑↓青↓）"),
        (0.8, 0.9, 1.3, "rgb_08_cool_tone.jpg", "寒色調整（赤↓緑↓青↑）"),
    ]
    
    for i, (r, g, b, filename, desc) in enumerate(rgb_tests, 1):
        print(f"\n{i}. {desc}")
        result = EffectLibrary.adjust_rgb_channels(original, r, g, b)
        save_result(result, filename, f"RGB調整: R={r:.1f}, G={g:.1f}, B={b:.1f}")


def test_rgb_offset_operations():
    """RGBオフセット調整テスト"""
    print(f"\n🌈 RGBオフセット調整テスト")
    print("=" * 50)
    
    original = load_test_image()
    if original is None:
        return
    
    # RGBオフセット調整テスト
    offset_tests = [
        # (r_offset, g_offset, b_offset, filename, description)
        (30, 0, 0, "rgb_09_red_offset_plus.jpg", "赤チャンネル +30"),
        (-30, 0, 0, "rgb_10_red_offset_minus.jpg", "赤チャンネル -30"),
        (0, 30, 0, "rgb_11_green_offset_plus.jpg", "緑チャンネル +30"),
        (0, -30, 0, "rgb_12_green_offset_minus.jpg", "緑チャンネル -30"),
        (0, 0, 30, "rgb_13_blue_offset_plus.jpg", "青チャンネル +30"),
        (0, 0, -30, "rgb_14_blue_offset_minus.jpg", "青チャンネル -30"),
        (20, -10, -10, "rgb_15_warm_offset.jpg", "暖色オフセット"),
        (-20, -10, 30, "rgb_16_cool_offset.jpg", "寒色オフセット"),
    ]
    
    for i, (r, g, b, filename, desc) in enumerate(offset_tests, 1):
        print(f"\n{i}. {desc}")
        result = EffectLibrary.adjust_rgb_offset(original, r, g, b)
        save_result(result, filename, f"RGBオフセット: R{r:+d}, G{g:+d}, B{b:+d}")


def test_color_balance():
    """カラーバランス調整テスト"""
    print(f"\n⚖️  カラーバランス調整テスト")
    print("=" * 50)
    
    original = load_test_image()
    if original is None:
        return
    
    # カラーバランステスト
    balance_tests = [
        # (shadows, midtones, highlights, filename, description)
        ((1.2, 0.9, 0.8), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), "rgb_17_warm_shadows.jpg", "シャドウ暖色調整"),
        ((0.8, 0.9, 1.2), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), "rgb_18_cool_shadows.jpg", "シャドウ寒色調整"),
        ((1.0, 1.0, 1.0), (1.2, 0.9, 0.8), (1.0, 1.0, 1.0), "rgb_19_warm_midtones.jpg", "ミッドトーン暖色調整"),
        ((1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.2, 0.9, 0.8), "rgb_20_warm_highlights.jpg", "ハイライト暖色調整"),
        ((0.9, 0.95, 1.1), (1.05, 1.0, 0.95), (1.1, 1.05, 0.9), "rgb_21_cinematic_balance.jpg", "シネマティックバランス"),
    ]
    
    for i, (shadows, midtones, highlights, filename, desc) in enumerate(balance_tests, 1):
        print(f"\n{i}. {desc}")
        result = EffectLibrary.color_balance(original, shadows, midtones, highlights)
        save_result(result, filename, desc)


def test_hue_saturation():
    """色相・彩度調整テスト"""
    print(f"\n🌺 色相・彩度調整テスト")
    print("=" * 50)
    
    original = load_test_image()
    if original is None:
        return
    
    # 色相シフトテスト
    hue_tests = [
        (-60, "rgb_22_hue_minus60.jpg", "色相 -60度（青→緑方向）"),
        (-30, "rgb_23_hue_minus30.jpg", "色相 -30度"),
        (30, "rgb_24_hue_plus30.jpg", "色相 +30度"),
        (60, "rgb_25_hue_plus60.jpg", "色相 +60度（青→紫方向）"),
        (120, "rgb_26_hue_plus120.jpg", "色相 +120度（補色反転）"),
        (180, "rgb_27_hue_plus180.jpg", "色相 +180度（完全反転）"),
    ]
    
    for shift, filename, desc in hue_tests:
        print(f"\n色相シフト: {desc}")
        result = EffectLibrary.hue_shift(original, shift)
        save_result(result, filename, desc)
    
    # 彩度調整テスト
    saturation_tests = [
        (0.0, "rgb_28_saturation_0.jpg", "彩度 0（完全グレースケール）"),
        (0.5, "rgb_29_saturation_05.jpg", "彩度 0.5（低彩度）"),
        (1.5, "rgb_30_saturation_15.jpg", "彩度 1.5（高彩度）"),
        (2.0, "rgb_31_saturation_20.jpg", "彩度 2.0（最大彩度）"),
    ]
    
    for factor, filename, desc in saturation_tests:
        print(f"\n彩度調整: {desc}")
        result = EffectLibrary.saturation_adjust(original, factor)
        save_result(result, filename, desc)


def test_creative_color_effects():
    """創造的色彩エフェクトテスト"""
    print(f"\n✨ 創造的色彩エフェクトテスト")
    print("=" * 50)
    
    original = load_test_image()
    if original is None:
        return
    
    # セピア効果
    print("\n1. セピア効果")
    sepia_light = EffectLibrary.sepia_effect(original, 0.5)
    sepia_full = EffectLibrary.sepia_effect(original, 1.0)
    save_result(sepia_light, "rgb_32_sepia_light.jpg", "セピア効果（軽微）")
    save_result(sepia_full, "rgb_33_sepia_full.jpg", "セピア効果（完全）")
    
    # モノクローム着色
    print("\n2. モノクローム着色")
    mono_warm = EffectLibrary.monochrome_tint(original, (255, 220, 180), 0.8)
    mono_cool = EffectLibrary.monochrome_tint(original, (180, 200, 255), 0.8)
    mono_green = EffectLibrary.monochrome_tint(original, (180, 255, 180), 0.8)
    save_result(mono_warm, "rgb_34_mono_warm.jpg", "モノクローム（暖色）")
    save_result(mono_cool, "rgb_35_mono_cool.jpg", "モノクローム（寒色）")
    save_result(mono_green, "rgb_36_mono_green.jpg", "モノクローム（緑）")
    
    # 映画的カラーグレーディング
    print("\n3. 映画的カラーグレーディング")
    cinema_warm = EffectLibrary.color_grade_cinematic(original, 'warm', 0.7)
    cinema_cool = EffectLibrary.color_grade_cinematic(original, 'cool', 0.7)
    cinema_vintage = EffectLibrary.color_grade_cinematic(original, 'vintage', 0.7)
    save_result(cinema_warm, "rgb_37_cinema_warm.jpg", "シネマティック（暖色系）")
    save_result(cinema_cool, "rgb_38_cinema_cool.jpg", "シネマティック（寒色系）")
    save_result(cinema_vintage, "rgb_39_cinema_vintage.jpg", "シネマティック（ヴィンテージ）")
    
    # 特定色置換
    print("\n4. 特定色置換")
    # 赤を緑に置換
    color_replace = EffectLibrary.selective_color_replace(
        original, 
        target_color=(255, 100, 100),  # 赤系
        replacement_color=(100, 255, 100),  # 緑系
        threshold=50.0
    )
    save_result(color_replace, "rgb_40_color_replace.jpg", "特定色置換（赤→緑）")


def test_phenomenological_color_instructions():
    """現象学的色彩指示テスト"""
    print(f"\n🧠 現象学的色彩指示テスト")
    print("=" * 50)
    
    original = load_test_image()
    if original is None:
        return
    
    editor = PhenomenologicalImageEditor()
    
    # 現象学的色彩指示
    color_instructions = [
        {
            'action': '記憶の色調を表現する',
            'location': '画像全体',
            'dimension': ['conceptual', 'temporal'],
            'intensity': 0.8,
            'filename': 'rgb_41_memory_tone.jpg',
            'description': '記憶の色調表現'
        },
        {
            'action': '感情の暖かさを色彩で表現',
            'location': '画像全体',
            'dimension': ['synesthetic', 'conceptual'],
            'intensity': 0.7,
            'filename': 'rgb_42_emotional_warmth.jpg',
            'description': '感情の暖色表現'
        },
        {
            'action': '色相を回転させて時間の変化を表現',
            'location': '画像全体',
            'dimension': ['temporal', 'appearance'],
            'intensity': 0.6,
            'filename': 'rgb_43_temporal_hue.jpg',
            'description': '時間変化の色相表現'
        },
        {
            'action': '彩度を調整して意識の明瞭さを表現',
            'location': '中央部',
            'dimension': ['appearance', 'ontological'],
            'intensity': 0.9,
            'filename': 'rgb_44_consciousness_saturation.jpg',
            'description': '意識の明瞭さ（彩度調整）'
        },
        {
            'action': 'セピア効果で過去の質感を表現',
            'location': '画像全体',
            'dimension': ['temporal', 'synesthetic'],
            'intensity': 0.8,
            'filename': 'rgb_45_past_sepia.jpg',
            'description': '過去の質感（セピア）'
        }
    ]
    
    for i, instruction in enumerate(color_instructions, 1):
        print(f"\n{i}. {instruction['description']}")
        print(f"   指示: {instruction['action']}")
        
        result = editor.apply_phenomenological_edit(original, instruction)
        save_result(result, instruction['filename'], instruction['description'])
        
        # 適用されたエフェクトの確認
        if editor.edit_history:
            last_edit = editor.edit_history[-1]
            effects = last_edit.get('effects', [])
            print(f"   → 適用エフェクト: {len(effects)}個")
            for effect in effects:
                print(f"     • {effect['name']} (強度: {effect['intensity']:.2f})")


def show_results_summary():
    """結果サマリーの表示"""
    print(f"\n📋 RGB色彩編集テスト結果サマリー")
    print("=" * 50)
    
    output_dir = Path("output")
    rgb_files = list(output_dir.glob("rgb_*.jpg"))
    
    if rgb_files:
        print(f"生成された RGB編集画像: {len(rgb_files)}個")
        
        categories = {
            "基本RGB調整": [f for f in rgb_files if f.name.startswith("rgb_0") and int(f.name.split('_')[1]) <= 8],
            "RGBオフセット": [f for f in rgb_files if f.name.startswith("rgb_") and 9 <= int(f.name.split('_')[1]) <= 16],
            "カラーバランス": [f for f in rgb_files if f.name.startswith("rgb_") and 17 <= int(f.name.split('_')[1]) <= 21],
            "色相・彩度": [f for f in rgb_files if f.name.startswith("rgb_") and 22 <= int(f.name.split('_')[1]) <= 31],
            "創造的エフェクト": [f for f in rgb_files if f.name.startswith("rgb_") and 32 <= int(f.name.split('_')[1]) <= 40],
            "現象学的指示": [f for f in rgb_files if f.name.startswith("rgb_") and 41 <= int(f.name.split('_')[1]) <= 45]
        }
        
        for category, files in categories.items():
            if files:
                print(f"\n{category}: {len(files)}個")
                for file in sorted(files):
                    size_kb = file.stat().st_size / 1024
                    print(f"  • {file.name} ({size_kb:.1f} KB)")
    
    print(f"\n💡 新しく追加されたRGB色彩編集機能:")
    print("  • adjust_rgb_channels - RGBチャンネル個別調整")
    print("  • adjust_rgb_offset - RGBオフセット調整")
    print("  • color_balance - シャドウ・ミッドトーン・ハイライト調整")
    print("  • hue_shift - 色相シフト")
    print("  • saturation_adjust - 彩度調整")
    print("  • selective_color_replace - 特定色置換")
    print("  • channel_mixer - RGBチャンネルミキサー")
    print("  • sepia_effect - セピア効果")
    print("  • monochrome_tint - モノクローム着色")
    print("  • color_grade_cinematic - 映画的カラーグレーディング")


def main():
    """メイン実行関数"""
    print("🎨 RGB色彩編集機能 - 包括的テスト")
    print("=" * 60)
    
    try:
        test_basic_rgb_operations()
        test_rgb_offset_operations()
        test_color_balance()
        test_hue_saturation()
        test_creative_color_effects()
        test_phenomenological_color_instructions()
        
        show_results_summary()
        
        print(f"\n{'=' * 60}")
        print("🎉 RGB色彩編集機能のテストが完了しました！")
        print("\n🌈 これで現象学的オラクルシステムは:")
        print("  • 基本的な画像エフェクト（13種類）")
        print("  • RGB色彩編集機能（10種類）")
        print("  • 現象学的指示の自動解釈")
        print("  • 合計23種類以上の豊富なエフェクト")
        print("\nを備えた強力な画像編集システムになりました！")
        
    except Exception as e:
        print(f"\n❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()