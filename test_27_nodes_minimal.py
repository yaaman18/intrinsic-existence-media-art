#!/usr/bin/env python3
"""
27ノード現象学的画像エフェクトシステムの最小限テスト
軽量で高速な動作確認
"""

import sys
import numpy as np
from pathlib import Path
from PIL import Image

# パスの設定
sys.path.append(str(Path(__file__).parent / "src" / "core"))

# 基本エフェクトライブラリのテスト
from base_effect_library import BaseEffectLibrary, ColorSpaceUtils, MaskOperations


def test_base_effects():
    """基本エフェクトライブラリのテスト"""
    print("🧪 基本エフェクトライブラリテスト")
    print("=" * 40)
    
    # テスト画像の読み込み
    image_path = Path("examples/images/shibuya-1.jpg")
    if not image_path.exists():
        print(f"❌ テスト画像が見つかりません: {image_path}")
        return False
    
    # 小さい画像にリサイズして処理を軽量化
    image = Image.open(image_path)
    image = image.resize((400, 300))  # より小さくリサイズ
    print(f"✅ テスト画像読み込み（リサイズ後）: {image.size}")
    
    # 出力ディレクトリの作成
    output_dir = Path("output/27nodes_minimal_test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 基本エフェクトのテスト
    test_cases = [
        ("RGBチャンネル調整", lambda img: BaseEffectLibrary.adjust_rgb_channels(img, 1.2, 0.9, 0.8)),
        ("色相シフト", lambda img: BaseEffectLibrary.hue_shift(img, 30)),
        ("彩度調整", lambda img: BaseEffectLibrary.saturation_adjust(img, 1.5)),
        ("輝度調整", lambda img: BaseEffectLibrary.luminosity_adjust(img, 1.2)),
        ("ガウシアンブラー", lambda img: BaseEffectLibrary.gaussian_blur(img, 3.0)),
        ("エッジ強調", lambda img: BaseEffectLibrary.edge_enhance(img, 0.5)),
    ]
    
    success_count = 0
    
    for i, (name, effect_func) in enumerate(test_cases, 1):
        print(f"\n{i}. {name}")
        
        try:
            # エフェクトの適用
            result_image = effect_func(image)
            
            # 結果の保存
            filename = f"base_effect_{i:02d}_{name.replace(' ', '_')}.jpg"
            output_path = output_dir / filename
            result_image.save(output_path, quality=85)
            
            print(f"   ✅ 保存完了: {filename}")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ エラー: {e}")
    
    print(f"\n{'='*40}")
    print(f"🎯 基本エフェクト結果: {success_count}/{len(test_cases)} 成功")
    
    return success_count == len(test_cases)


def test_mask_operations():
    """マスク操作のテスト"""
    print("\n🧪 マスク操作テスト")
    print("=" * 40)
    
    # テスト用のマスクサイズ
    size = (300, 400)  # height, width
    
    masks = [
        ("円形マスク", MaskOperations.create_circular_mask(size, (0.5, 0.5), 0.3, 0.1)),
        ("グラデーションマスク（垂直）", MaskOperations.create_gradient_mask(size, "vertical")),
        ("グラデーションマスク（水平）", MaskOperations.create_gradient_mask(size, "horizontal")),
        ("グラデーションマスク（放射）", MaskOperations.create_gradient_mask(size, "radial")),
    ]
    
    output_dir = Path("output/27nodes_minimal_test")
    success_count = 0
    
    for i, (name, mask) in enumerate(masks, 1):
        print(f"\n{i}. {name}")
        
        try:
            # マスクを画像として保存
            mask_image = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
            filename = f"mask_{i:02d}_{name.replace(' ', '_').replace('（', '_').replace('）', '')}.jpg"
            output_path = output_dir / filename
            mask_image.save(output_path, quality=85)
            
            print(f"   ✅ マスク保存: {filename}")
            print(f"   形状: {mask.shape}, 値範囲: {mask.min():.2f}-{mask.max():.2f}")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ エラー: {e}")
    
    print(f"\n{'='*40}")
    print(f"🎯 マスク操作結果: {success_count}/{len(masks)} 成功")
    
    return success_count == len(masks)


def test_color_space_utils():
    """色空間変換ユーティリティのテスト"""
    print("\n🧪 色空間変換テスト")
    print("=" * 40)
    
    # 小さなテスト画像を作成
    test_image = Image.new('RGB', (100, 100), (128, 64, 192))
    test_array = np.array(test_image)
    
    conversions = [
        ("RGB → HSV → RGB", lambda arr: ColorSpaceUtils.hsv_to_rgb_array(ColorSpaceUtils.rgb_to_hsv_array(arr))),
        ("RGB → LAB → RGB", lambda arr: ColorSpaceUtils.lab_to_rgb_array(ColorSpaceUtils.rgb_to_lab_array(arr))),
    ]
    
    success_count = 0
    
    for i, (name, conversion_func) in enumerate(conversions, 1):
        print(f"\n{i}. {name}")
        
        try:
            # 変換実行
            converted = conversion_func(test_array)
            
            # 変換後の画像を保存
            converted_image = Image.fromarray(converted)
            filename = f"colorspace_{i:02d}_{name.split(' ')[0]}_conversion.jpg"
            output_path = Path("output/27nodes_minimal_test") / filename
            converted_image.save(output_path, quality=85)
            
            # データの整合性チェック
            difference = np.mean(np.abs(test_array.astype(float) - converted.astype(float)))
            print(f"   ✅ 変換完了: {filename}")
            print(f"   平均誤差: {difference:.2f}")
            
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ エラー: {e}")
    
    print(f"\n{'='*40}")
    print(f"🎯 色空間変換結果: {success_count}/{len(conversions)} 成功")
    
    return success_count == len(conversions)


def show_generated_files():
    """生成されたファイルの表示"""
    print("\n📁 生成されたファイル")
    print("=" * 40)
    
    output_dir = Path("output/27nodes_minimal_test")
    if not output_dir.exists():
        print("出力ディレクトリが見つかりません")
        return
    
    files = list(output_dir.glob("*.jpg"))
    if not files:
        print("生成されたファイルが見つかりません")
        return
    
    total_size = 0
    for file_path in sorted(files):
        size_kb = file_path.stat().st_size / 1024
        total_size += size_kb
        print(f"   {file_path.name} ({size_kb:.1f}KB)")
    
    print(f"\n合計: {len(files)}ファイル, {total_size/1024:.2f}MB")


def main():
    """メインテスト実行"""
    print("🚀 27ノード現象学的画像エフェクトシステム - 最小限テスト")
    print("=" * 60)
    
    results = []
    
    # 基本エフェクトライブラリテスト
    result1 = test_base_effects()
    results.append(("基本エフェクトライブラリ", result1))
    
    # マスク操作テスト
    result2 = test_mask_operations()
    results.append(("マスク操作", result2))
    
    # 色空間変換テスト
    result3 = test_color_space_utils()
    results.append(("色空間変換", result3))
    
    # ファイル表示
    show_generated_files()
    
    # 総合結果
    print(f"\n{'='*60}")
    print("🏁 総合結果")
    print("="*60)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    print(f"\n📊 成功率: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n🎉 基盤システムが正常に動作しています！")
        print("\n💡 基盤システム確認完了:")
        print("   ✅ BaseEffectLibrary - RGB/HSV/LAB色空間処理")
        print("   ✅ MaskOperations - 各種マスク生成")
        print("   ✅ ColorSpaceUtils - 色空間変換")
        print("\n🔄 次は現出様式エフェクトの簡略版実装に進めます")
    else:
        print(f"\n⚠️  基盤システムに問題があります。修正が必要です。")
        
    return success_count == total_count


if __name__ == "__main__":
    main()