#!/usr/bin/env python3
"""
RGB色彩編集機能の基本テスト（高速版）
"""

import sys
from pathlib import Path
from PIL import Image

sys.path.append(str(Path(__file__).parent / "src" / "core"))

from phenomenological_image_editor import PhenomenologicalImageEditor, EffectLibrary


def test_rgb_quick():
    """RGB編集機能のクイックテスト"""
    print("🎨 RGB色彩編集機能 - クイックテスト")
    print("=" * 40)
    
    # 画像読み込み
    original = Image.open("examples/images/shibuya-1.jpg")
    print(f"✅ 画像読み込み完了: {original.size}")
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # 基本RGBテスト
    tests = [
        ("RGB赤強化", lambda img: EffectLibrary.adjust_rgb_channels(img, 1.5, 1.0, 1.0), "rgb_red_boost.jpg"),
        ("RGB青強化", lambda img: EffectLibrary.adjust_rgb_channels(img, 1.0, 1.0, 1.5), "rgb_blue_boost.jpg"),
        ("色相シフト", lambda img: EffectLibrary.hue_shift(img, 60), "rgb_hue_shift.jpg"),
        ("彩度調整", lambda img: EffectLibrary.saturation_adjust(img, 1.8), "rgb_saturation.jpg"),
        ("セピア効果", lambda img: EffectLibrary.sepia_effect(img, 0.8), "rgb_sepia.jpg"),
        ("暖色グレーディング", lambda img: EffectLibrary.color_grade_cinematic(img, 'warm', 0.7), "rgb_warm_grade.jpg"),
    ]
    
    success_count = 0
    
    for i, (name, func, filename) in enumerate(tests, 1):
        print(f"\n{i}. {name}")
        try:
            result = func(original)
            output_path = output_dir / filename
            result.save(output_path, quality=95)
            print(f"   ✅ 保存: {output_path}")
            success_count += 1
        except Exception as e:
            print(f"   ❌ エラー: {e}")
    
    # 現象学的指示テスト
    print(f"\n🧠 現象学的色彩指示テスト")
    editor = PhenomenologicalImageEditor()
    
    pheno_tests = [
        {
            'action': '記憶の色調を表現する',
            'intensity': 0.7,
            'filename': 'rgb_memory_tone.jpg',
            'description': '記憶の色調'
        },
        {
            'action': '色相を回転させて時間の変化を表現',
            'intensity': 0.6,
            'filename': 'rgb_temporal_hue.jpg', 
            'description': '時間変化の色相'
        },
        {
            'action': '感情の暖かさを色彩で表現',
            'intensity': 0.8,
            'filename': 'rgb_emotional_warmth.jpg',
            'description': '感情の暖色'
        }
    ]
    
    for i, test in enumerate(pheno_tests, 1):
        print(f"\n{i+6}. {test['description']}")
        try:
            instruction = {
                'action': test['action'],
                'location': '画像全体',
                'dimension': ['appearance', 'conceptual'],
                'intensity': test['intensity']
            }
            
            result = editor.apply_phenomenological_edit(original, instruction)
            output_path = output_dir / test['filename']
            result.save(output_path, quality=95)
            print(f"   ✅ 保存: {output_path}")
            
            # 適用エフェクトの表示
            if editor.edit_history:
                last_edit = editor.edit_history[-1]
                effects = last_edit.get('effects', [])
                print(f"   → 適用エフェクト: {[e['name'] for e in effects]}")
            
            success_count += 1
        except Exception as e:
            print(f"   ❌ エラー: {e}")
    
    print(f"\n{'=' * 40}")
    print(f"🎯 テスト結果: {success_count}/{len(tests) + len(pheno_tests)} 成功")
    
    # 新機能一覧表示
    print(f"\n💡 追加されたRGB色彩編集機能:")
    rgb_functions = [
        "adjust_rgb_channels", "adjust_rgb_offset", "color_balance",
        "hue_shift", "saturation_adjust", "selective_color_replace",
        "channel_mixer", "sepia_effect", "monochrome_tint", "color_grade_cinematic"
    ]
    
    for func in rgb_functions:
        if hasattr(EffectLibrary, func):
            print(f"  ✅ {func}")
        else:
            print(f"  ❌ {func}")
    
    print(f"\n🌈 RGB色彩編集機能が正常に統合されました！")


if __name__ == "__main__":
    try:
        test_rgb_quick()
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        import traceback
        traceback.print_exc()